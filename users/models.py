from django.contrib.auth.models import AbstractUser
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
    phone = models.CharField(
        max_length=35, blank=True, null=True, help_text="Введите номер телефона"
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


class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ("cash", "Наличные"),
        ("transfer", "Перевод на счет"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="payments",
        verbose_name="Пользователь",
    )
    payment_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата оплаты")
    paid_course = models.ForeignKey(
        "courses.Course",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="payments",
        verbose_name="Оплаченный курс",
    )
    paid_lesson = models.ForeignKey(
        "courses.Lesson",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="payments",
        verbose_name="Оплаченный урок",
    )
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Сумма оплаты"
    )
    payment_method = models.CharField(
        max_length=10, choices=PAYMENT_METHOD_CHOICES, verbose_name="Способ оплаты"
    )

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"
