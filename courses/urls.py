from django.urls import path
from .views import IndexView, CourseListView, ReviewCreateView, mercado_pago_webhook, exam_view, CertificatePDFPrintView, CertificatesListView
from django.views.generic import TemplateView

app_name = 'courses'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('course/<int:pk>/', ReviewCreateView.as_view(), name='course-detail'),
    path('course/my_courses/', CourseListView.as_view(), name='my-courses'),
    path('course/my_certificates/', CertificatesListView.as_view(), name='my-certificates'),
    path('course/mercado_pago_webhook/', mercado_pago_webhook, name='mercado-pago-webhook'),
    path('course/<int:course_id>/exam', exam_view, name='exam'),
    path('course/<int:pk>/pdf/', CertificatePDFPrintView.as_view(), name='certificate-pdf')
]