from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model, logout
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.views.generic import View
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from .forms import RegistrationForm, UserProfileForm

# User = get_user_model()
# def activate(request, uidb64, token):
#     try:
#         uid = force_str(urlsafe_base64_decode(uidb64))
#         user = User.objects.get(pk=uid)
#     except:
#         user = None
#     print(user, uid)
#     print(f'{account_activation_token.check_token(user, token)=}')
#     if user is not None and account_activation_token.check_token(user, token):
#         user.is_active = True
#         user.save()
#         messages.success(request, "Tu email ha sido verificado, ahora puedes iniciar sesion")
#         return redirect('users:login')
#     else:
#         messages.error(request, "Link de activacion es invalido")
#         return redirect('courses:index')

# def activate_email(request, user, to_email):
#     mail_subject = "Activa tu cuenta"
#     message = render_to_string("users/activate_account.html", {
#         'user': user,
#         'domain': get_current_site(request).domain,
#         'uid': urlsafe_base64_encode(force_bytes(user.pk)),
#         'token': account_activation_token.make_token(user),
#         'protocol': 'https' if request.is_secure() else 'http'
#     })
#     email = EmailMessage(mail_subject, message, to=[to_email])
#     if email.send():
#         messages.success(request, f'{user.full_name} te hemos enviado un correo de verificacion a {user.email}')
#     else:
#         messages.error(request, f'Hubo un problema al enviar el correo a {user.email}')

# # Create your views here.
# def signup(request):
#     if request.method == 'POST':
#         form = RegistrationForm(request.POST)
#         if form.is_valid():
#             new_account = form.save(commit=False)
#             new_account.is_active = False
#             new_account.save()
#             activate_email(request, new_account, form.cleaned_data.get('email'))
#             return redirect("users:login")
#         else:
#             return render(request, 'users/signup.html', {
#                 'form': form,
#             })
#     else:
#         return render(request, 'users/signup.html', {
#             'form': RegistrationForm(),
#         })

# class LogoutUser(View):
#     def get(self, request, *args, **kwargs):
#         logout(self.request)
#         return redirect('users:login')

def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Tu perfil ha sido actualizado")
            return redirect("users:profile")
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, 'users/profile.html', {
        'form': form,
    })