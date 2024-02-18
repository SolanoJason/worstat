from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, User, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

# Create your models here.

class AccountManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Users must have an email addres')
        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email=self.normalize_email(email), password=password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
            

class Account(AbstractBaseUser, PermissionsMixin):
    full_name = models.CharField("Nombre completo", max_length=150)
    email = models.EmailField("Correo electronico", unique=True)
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), auto_now_add=True)
    picture = models.ImageField(max_length=500, upload_to='users', null=True, blank=True)
    about = models.TextField("Biografia", blank=True)

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = AccountManager()

    class Meta:
        verbose_name = "Cuenta"
        verbose_name_plural = "Cuentas"

    def __str__(self) -> str:
        return f'{self.email}'

class Contact(models.Model):
    email = models.EmailField("Correo electronico")
    about = models.CharField(max_length=255, verbose_name='A cerca de')
    message = models.TextField(verbose_name='Mensage')

    class Meta:
        verbose_name = 'Contacto'
        verbose_name_plural = 'Contactos'