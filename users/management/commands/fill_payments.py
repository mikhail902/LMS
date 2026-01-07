from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from courses.models import Course, Lesson
from users.models import Payment
from datetime import datetime, timedelta
import random

User = get_user_model()


class Command(BaseCommand):
    help = "Создает тестовые платежи используя email пользователей"

    def handle(self, *args, **options):
        self.stdout.write("Создание платежей с использованием email...")

        # 1. Получаем пользователей по email
        test_emails = [
            "admin@example.com",  # ваш админ
            "ivan@example.com",  # тестовый пользователь 1
            "maria@example.com",  # тестовый пользователь 2
        ]

        users = []
        for email in test_emails:
            try:
                user = User.objects.get(email=email)
                users.append(user)
                self.stdout.write(f"✅ Найден пользователь: {email}")
            except User.DoesNotExist:
                self.stdout.write(f"⚠️ Пользователь {email} не найден. Создаю...")
                user = User.objects.create(
                    email=email,
                    first_name=email.split("@")[0].capitalize(),
                    last_name="Тестовый",
                    is_active=True,
                )
                user.set_password("12345")
                user.save()
                users.append(user)

        if not users:
            self.stdout.write(
                self.style.ERROR("❌ Нет пользователей для создания платежей!")
            )
            return

        # 2. Создаем тестовые курсы если нет
        if not Course.objects.exists():
            self.stdout.write("Создаю тестовые курсы...")
            Course.objects.create(
                title="Python для начинающих",
                description="Основы программирования на Python",
            )
            Course.objects.create(
                title="Django разработка",
                description="Создание веб-приложений на Django",
            )

        courses = list(Course.objects.all())

        # 3. Создаем тестовые уроки если нет
        if not Lesson.objects.exists():
            self.stdout.write("Создаю тестовые уроки...")
            for course in courses:
                Lesson.objects.create(
                    title=f"{course.title} - Введение",
                    description=f"Вводный урок курса {course.title}",
                    course=course,
                    video_url="https://example.com/video/1",
                )

        lessons = list(Lesson.objects.all())

        # 4. Очищаем старые платежи (опционально)
        Payment.objects.all().delete()
        self.stdout.write("Старые платежи удалены")

        # 5. Создаем платежи
        payments_to_create = []

        for i, user in enumerate(users):
            self.stdout.write(f"\nСоздаю платежи для {user.email}:")

            # Создаем 1-2 платежа на пользователя
            for j in range(random.randint(1, 2)):
                # Случайно выбираем курс или урок
                if random.choice([True, False]) and courses:
                    paid_course = random.choice(courses)
                    paid_lesson = None
                    item_name = f'курс "{paid_course.title}"'
                    amount = random.randint(10000, 30000)
                elif lessons:
                    paid_course = None
                    paid_lesson = random.choice(lessons)
                    item_name = f'урок "{paid_lesson.title}"'
                    amount = random.randint(1000, 5000)
                else:
                    continue

                # Случайная дата
                days_ago = random.randint(1, 30)
                payment_date = datetime.now() - timedelta(
                    days=days_ago,
                    hours=random.randint(0, 23),
                    minutes=random.randint(0, 59),
                )

                payment_method = random.choice(["cash", "transfer"])

                payments_to_create.append(
                    Payment(
                        user=user,
                        payment_date=payment_date,
                        paid_course=paid_course,
                        paid_lesson=paid_lesson,
                        amount=amount,
                        payment_method=payment_method,
                    )
                )

                self.stdout.write(f"  - {item_name}: {amount} руб. ({payment_method})")

        # 6. Сохраняем все платежи
        if payments_to_create:
            Payment.objects.bulk_create(payments_to_create)
            self.stdout.write(
                self.style.SUCCESS(
                    f"\n✅ Успешно создано {len(payments_to_create)} платежей!"
                )
            )

            # Выводим информацию о созданных платежах
            self.print_payments_summary()
        else:
            self.stdout.write(self.style.WARNING("⚠️ Не создано ни одного платежа"))

    def print_payments_summary(self):
        """Выводит сводку по созданным платежам"""
        payments = Payment.objects.all().order_by("-payment_date")

        self.stdout.write("\n" + "=" * 60)
        self.stdout.write("СОЗДАННЫЕ ПЛАТЕЖИ:")
        self.stdout.write("=" * 60)

        for payment in payments:
            if payment.paid_course:
                item = f"Курс: {payment.paid_course.title}"
            else:
                item = f"Урок: {payment.paid_lesson.title}"

            self.stdout.write(
                f"👤 {payment.user.email}\n"
                f"   {item}\n"
                f"   💰 {payment.amount} руб. | "
                f"💳 {payment.get_payment_method_display()} | "
                f'📅 {payment.payment_date.strftime("%d.%m.%Y %H:%M")}\n'
                f'   {"-" * 40}'
            )

        # Статистика
        self.stdout.write("\n📊 СТАТИСТИКА:")
        self.stdout.write(f"   Всего платежей: {payments.count()}")
        self.stdout.write(
            f'   Наличными: {payments.filter(payment_method="cash").count()}'
        )
        self.stdout.write(
            f'   Переводом: {payments.filter(payment_method="transfer").count()}'
        )

        # Группировка по пользователям
        self.stdout.write("\n👥 ПОЛЬЗОВАТЕЛИ:")
        for payment in payments:
            user_payments = payments.filter(user=payment.user)
            if user_payments.exists():
                total = sum(p.amount for p in user_payments)
                self.stdout.write(
                    f"   {payment.user.email}: "
                    f"{user_payments.count()} платежей, "
                    f"итого {total} руб."
                )
                # Удаляем дубликаты
                payments = payments.exclude(user=payment.user)
