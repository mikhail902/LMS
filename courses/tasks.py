from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from courses.models import Subscription


@shared_task
def send_course_update_email(course_id):
    subscriptions = Subscription.objects.filter(course_id=course_id).select_related('user')
    emails = [sub.user.email for sub in subscriptions if sub.user.email]

    if emails:
        send_mail(
            subject='Курс обновлен',
            message=f'Курс с ID {course_id} был обновлен. Проверьте новые материалы!',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=emails,
            fail_silently=True,
        )
    return f'Отправлено {len(emails)} писем'