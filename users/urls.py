from django.urls import path
from .views import profile

app_name = 'users'

urlpatterns = [
    # path("signup/", signup, name="signup"),
    # path("login/", auth_views.LoginView.as_view(template_name = "users/login.html", redirect_authenticated_user = True), name='login'),
    # path("logout/", LogoutUser.as_view(), name='logout'),
    path("profile/", profile, name="profile"),
    # path("activate/<uidb64>/<token>", activate, name='activate')
]