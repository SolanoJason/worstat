from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from .models import Course, Section, Review, Question, Answer, Enrollment
from django.views.generic import ListView, DetailView, CreateView
from .forms import ReviewForm
import mercadopago
from django.http import HttpResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
import json
import functools
from django_weasyprint import WeasyTemplateResponseMixin
from django_weasyprint.views import WeasyTemplateResponse
from django_weasyprint.utils import django_url_fetcher
from django.utils import timezone
import ssl

class IndexView(ListView):
    """
    Vista de administracion
    """
    model = Course
    template_name = "courses/index.html"
    context_object_name = "courses"

class CertificatePDFDetailView(DetailView):
    model = Enrollment
    template_name = 'courses/certificate_pdf.html'
    context_object_name = 'enrollment'

class CustomWeasyTemplateResponse(WeasyTemplateResponse):
    """
    Vista que renderiza el pdf
    """
    # customized response class to change the default URL fetcher

    def get_url_fetcher(self):
        # disable host and certificate check
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        return functools.partial(django_url_fetcher, ssl_context=context)

class CertificatePDFPrintView(WeasyTemplateResponseMixin, CertificatePDFDetailView):
    """
    Vista que carga los estilos css al pdf
    """
    # output of PrescriptionView rendered as PDF with hardcoded CSS
    pdf_stylesheets = [
        'theme' + settings.STATIC_URL + 'css/certificate.css',
    ]
    # show pdf in-line (default: True, show download dialog)
    pdf_attachment = False
    # custom response class to configure url-fetcher
    response_class = CustomWeasyTemplateResponse

class CertificatePDFDownloadView(WeasyTemplateResponseMixin, CertificatePDFDetailView):
    """
    Vista para descargar en pdf
    """
    # suggested filename (is required for attachment/download!)
    pdf_filename = 'foo.pdf'

class CertificatePDFImageView(WeasyTemplateResponseMixin, CertificatePDFDetailView):
    """
    Vista para la prescripcion en imagen
    """
    # generate a PNG image instead

    # dynamically generate filename
    def get_pdf_filename(self):
        return 'foo-{at}.pdf'.format(
            at=timezone.now().strftime('%Y%m%d-%H%M'),
        )

@csrf_exempt
def mercado_pago_webhook(request):
    print("MERCADO PAGOOO")
    print(f'{request=}')
    if request.method == 'POST':
        print(f'{request.POST=}')
        print(f'{request.GET=}')
        print(f'{request.__dict__=}')
        print(f'{request.headers=}')
        print(f'{request.META=}')
        return HttpResponse(status=200, content='hola')
    else:
        return HttpResponse(status=405)

def exam_view(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    questions = Question.objects.filter(course=course)

    if request.method == 'POST':
        # Procesar las respuestas aquí
        score = 0
        total_questions = 0
        for question in questions:
            total_questions += 1
            selected_answerd_id = request.POST.get(f'question{question.id}')
            
            if selected_answerd_id:
                selected_answer = get_object_or_404(Answer, pk=selected_answerd_id)
                if selected_answer.is_correct:
                    score += 1
        
        if total_questions > 0:
            percentage_correct = (score / total_questions) * 100
        else:
            percentage_correct = 0

        if percentage_correct >= 80:
            enrollment = Enrollment.objects.get(user=request.user, course=course)
            enrollment.is_completed = True
            enrollment.save()
            messages.success(request, f"Haz completado el examen exitosamente con una puntuacion del {percentage_correct:.0f}%")
            return redirect("courses:my-certificates")
        else:
            messages.info(request, f"Necesitas una puntuacion de al menos 80% para pasar el examen, solo obtuviste {percentage_correct:.1f}.%")
            return redirect("courses:exam", course_id=course.id)

        # Redirigir o renderizar resultados según sea necesario
        return render(request, 'courses/exam_result.html', {'course': course, 'score': score, 'percentage_correct': percentage_correct})

    # Si no es una solicitud POST, mostrar el examen
    context = {'course': course, 'questions': questions}
    return render(request, 'courses/exam.html', context)


# def checkout(request, course_id):
#     course = Course.objects.get(pk=course_id)
#     return render(request, 'courses/checkout.html', {'course': course})

# def payment_successful(request, course_id):
#     course = Course.objects.get(pk=course_id)
#     return render(request, 'courses/payment-success.html', {'course': course})

# def payment_failed(request, course_id):
#     course = Course.objects.get(pk=course_id)
#     return render(request, 'courses/payment-failed.html', {'course': course})

# class CourseDetailView(CreateView):
#     model = Review
#     template_name = "courses/course.html"
#     fields = ['comment', 'rating']

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["course"] = Course.objects.get(pk=self.request['pk'])
#         return context

class ReviewCreateView(CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'courses/course.html'  # Update with your actual template path

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.course_id = self.kwargs['pk']
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('courses:course-detail', kwargs={'pk': self.kwargs['pk']})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = Course.objects.get(pk=self.kwargs['pk'])
        context["course"] = course
        context["reviews"] = Review.objects.filter(course=course)
        context['preference'] = json.loads(course.preference)
        context['PUBLIC_KEY'] = settings.MERCADO_PAGO_PUBLIC_KEY
        if self.request.user.is_authenticated:
            context['is_completed'] = self.request.user.enrollment_set.filter(course=course, is_completed=True).exists()
        return context
    
class CourseListView(ListView):
    model = Course
    template_name = 'courses/my_courses.html'
    context_object_name = 'courses'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context["courses"] = user.course_set.all()
        return context

class CertificatesListView(ListView):
    model = Enrollment
    template_name = 'courses/my_certificates.html'
    context_object_name = 'enrollments'

    def get_queryset(self):
        user = self.request.user
        return Enrollment.objects.filter(user=user, is_completed=True)

# Create your views here.

# class CourseList(generics.ListCreateAPIView):
#     queryset = Course.objects.all()
#     serializer_class = CourseSerializer

# class CourseDetail(generics.RetrieveAPIView):
#     queryset = Course.objects.all()
#     serializer_class = CourseSerializer

# class SectionList(generics.ListAPIView):
#     serializer_class = SectionSerializer

#     def get_queryset(self):
#         course_id = self.kwargs['course_id']  # Assuming 'course_id' is the parameter in your URL
#         return Section.objects.filter(course__id=course_id)  # Assuming you have a ForeignKey 'course' in your Section model

    


