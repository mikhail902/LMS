from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from users.models import User


@shared_task
def check_inactive_users():
    month_ago = timezone.now() - timedelta(days=30)
    inactive_users = User.objects.filter(
        is_active=True,
        last_login__lt=month_ago
    )
    count = inactive_users.update(is_active=False)
    return f'Заблокировано пользователей: {count}'