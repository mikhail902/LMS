from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from courses.models import Course, Lesson


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"


class LessonDetailSerializer(ModelSerializer):
    lessons_with_same_course = SerializerMethodField()

    def get_lessons_with_same_course(self, lesson):
        return Lesson.objects.filter(course=lesson.course).count()

    class Meta:
        model = Lesson
        fields = (
            "title",
            "description",
            "preview",
            "course",
            "lessons_with_same_course",
        )


class CourseSerializer(ModelSerializer):
    lessons_count = SerializerMethodField()
    lessons = SerializerMethodField()

    def get_lessons_count(self, course):
        """Возвращает количество уроков в курсе"""
        return Lesson.objects.filter(course=course).count()

    def get_lessons(self, course):
        """Возвращает информацию по всем урокам курса"""
        lessons = Lesson.objects.filter(course=course)
        return LessonSerializer(lessons, many=True).data

    class Meta:
        model = Course
        fields = (
            "title",
            "description",
            "preview",
            "lessons_count",
            "lessons",
            "lessons_count",
            "lessons",
        )
