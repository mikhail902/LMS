from rest_framework import serializers

from courses.models import Course, Lesson

from .models import Payment, User


class PaymentSerializer(serializers.ModelSerializer):
    # Добавляем дополнительные поля для удобства
    user_email = serializers.EmailField(source="user.email", read_only=True)
    user_full_name = serializers.SerializerMethodField()
    course_title = serializers.CharField(
        source="paid_course.title", read_only=True, allow_null=True
    )
    lesson_title = serializers.CharField(
        source="paid_lesson.title", read_only=True, allow_null=True
    )

    def get_user_full_name(self, obj):
        return obj.user.get_full_name()

    class Meta:
        model = Payment
        fields = [
            "id",
            "user",
            "user_email",
            "user_full_name",
            "payment_date",
            "paid_course",
            "paid_lesson",
            "course_title",
            "lesson_title",
            "amount",
            "payment_method",
            "get_payment_method_display",
        ]
        read_only_fields = ["payment_date"]
