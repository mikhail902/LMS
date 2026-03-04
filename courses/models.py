from django.db import models
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from users.models import User
class Course(models.Model):
    """Модель курса"""

    title = models.CharField(_("title"), max_length=200, help_text=_("Название курса"))

    preview = models.ImageField(
        _("preview image"),
        upload_to="courses/previews/",
        blank=True,
        null=True,
        help_text=_("Превью-изображение курса"),
    )

    description = models.TextField(
        _("description"), help_text=_("Подробное описание курса")
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses', null=True, blank=True)

    class Meta:
        verbose_name = _("course")
        verbose_name_plural = _("courses")

    def __str__(self):
        return self.title


class Lesson(models.Model):
    """Модель урока"""

    title = models.CharField(_("title"), max_length=200, help_text=_("Название урока"))

    description = models.TextField(
        _("description"), help_text=_("Подробное описание урока")
    )

    preview = models.ImageField(
        _("preview image"),
        upload_to="lessons/previews/",
        blank=True,
        null=True,
        help_text=_("Превью-изображение урока"),
    )

    video_url = models.URLField(
        _("video URL"), blank=True, null=True, help_text=_("Ссылка на видео урока")
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="lessons",
        verbose_name=_("course"),
        help_text=_("Курс, к которому принадлежит урок"),
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lessons', null=True, blank=True)

    class Meta:
        verbose_name = _("lesson")
        verbose_name_plural = _("lessons")

    def __str__(self):
        return f"{self.title}"
