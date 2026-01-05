from django.core.cache import cache
from django.shortcuts import get_object_or_404

from courses.models import Course, Lesson


def get_lesson_by_course(course_id):
    """
    Сервисная функция для получения всех уроков в указанном курсе
    """
    course = get_object_or_404(Course, id=course_id)
    return Lesson.objects.filter(course=course)
