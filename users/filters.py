from django_filters import rest_framework as filters

from courses.models import Course, Lesson

from .models import Payment


class PaymentFilter(filters.FilterSet):
    course = filters.ModelChoiceFilter(
        field_name="paid_course", queryset=Course.objects.all(), label="Курс"
    )

    lesson = filters.ModelChoiceFilter(
        field_name="paid_lesson", queryset=Lesson.objects.all(), label="Урок"
    )

    payment_method = filters.ChoiceFilter(
        choices=Payment.PAYMENT_METHOD_CHOICES, label="Способ оплаты"
    )

    payment_date_from = filters.DateFilter(
        field_name="payment_date", lookup_expr="gte", label="Дата оплаты от"
    )
    payment_date_to = filters.DateFilter(
        field_name="payment_date", lookup_expr="lte", label="Дата оплаты до"
    )

    user_email = filters.CharFilter(
        field_name="user__email", lookup_expr="icontains", label="Email пользователя"
    )

    ordering = filters.OrderingFilter(
        fields=(
            ("payment_date", "payment_date"),
            ("amount", "amount"),
            ("user__email", "user_email"),
        ),
        field_labels={
            "payment_date": "Дата оплаты",
            "amount": "Сумма",
            "user__email": "Email пользователя",
        },
    )

    class Meta:
        model = Payment
        fields = [
            "course",
            "lesson",
            "payment_method",
            "payment_date_from",
            "payment_date_to",
            "user_email",
        ]
