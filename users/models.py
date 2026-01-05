from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """Модель пользователя с авторизацией по email"""

    username = models.CharField(
        max_length=150, unique=False, blank=True, null=True, verbose_name="username"
    )
    email = models.EmailField(
        _("email address"),
        unique=True,
        error_messages={
            "unique": _("Пользователь с таким email уже существует."),
        },
    )
    phone_regex = RegexValidator(
        regex=r"^\+?1?\d{9,15}$",
        message="Номер телефона должен быть в формате: '+999999999'. Максимум 15 цифр.",
    )
    phone = models.CharField(
        _("phone number"),
        validators=[phone_regex],
        max_length=17,
        blank=True,
        null=True,
    )
    city = models.CharField(_("city"), max_length=100, blank=True, null=True)

    avatar = models.ImageField(
        _("avatar"),
        upload_to="users/avatars/",
        blank=True,
        null=True,
        default="users/avatars/default.png",
    )
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email

    def get_full_name(self):
        """
        Возвращает полное имя пользователя
        """
        full_name = f"{self.first_name} {self.last_name}"
        return full_name.strip()

    def get_short_name(self):
        """
        Возвращает короткое имя пользователя
        """
        return self.first_name
