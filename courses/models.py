from django.db import models
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers


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

    class Meta:
        verbose_name = _("course")
        verbose_name_plural = _("courses")

    def __str__(self):
        return self.title

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = {
            'title',
            'descriptions',
        }

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

    class Meta:
        verbose_name = _("lesson")
        verbose_name_plural = _("lessons")

    def __str__(self):
        return f"{self.title}"

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = {
            'title',
            'descriptions',
        }
