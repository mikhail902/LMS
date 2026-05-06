from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer
from users.models import Payment
from courses.models import Course, Lesson, Subscription
from courses.validators import validate_youtube_link


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"
        extra_kwargs = {
            'video_url': {
                'validators': [validate_youtube_link],
            }
        }


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
    is_subscribed = SerializerMethodField()

    def get_lessons_count(self, course):
        """Возвращает количество уроков в курсе"""
        return Lesson.objects.filter(course=course).count()

    def get_lessons(self, course):
        """Возвращает информацию по всем урокам курса"""
        lessons = Lesson.objects.filter(course=course)
        return LessonSerializer(lessons, many=True).data

    def get_is_subscribed(self, obj):
        """Проверяет, подписан ли текущий пользователь на курс"""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Subscription.objects.filter(
                user=request.user, course=obj
            ).exists()
        return False

    class Meta:
        model = Course
        fields = (
            "title",
            "description",
            "preview",
            "lessons_count",
            "lessons",
            "is_subscribed",
        )

class PaymentSerializer(ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'