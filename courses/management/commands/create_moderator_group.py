from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from courses.models import Course, Lesson


class Command(BaseCommand):
    help = 'Создание группы модераторов с правами на просмотр и редактирование'

    def handle(self, *args, **options):

        moderator_group, created = Group.objects.get_or_create(name='moderators')

        if created:
            self.stdout.write(self.style.SUCCESS('Группа "moderators" создана'))

        course_content_type = ContentType.objects.get_for_model(Course)
        lesson_content_type = ContentType.objects.get_for_model(Lesson)

        permissions = Permission.objects.filter(
            content_type__in=[course_content_type, lesson_content_type],
            codename__in=[
                'view_course', 'change_course',
                'view_lesson', 'change_lesson'
            ]
        )

        moderator_group.permissions.set(permissions)

        self.stdout.write(
            self.style.SUCCESS('Права успешно добавлены группе "moderators"')
        )