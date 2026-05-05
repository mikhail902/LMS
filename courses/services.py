import stripe
from django.conf import settings
from courses.models import Lesson

stripe.api_key = settings.STRIPE_SECRET_KEY


def get_lesson_by_course(course_id):
    """Возвращает уроки по ID курса"""
    return Lesson.objects.filter(course_id=course_id)


def create_stripe_product(course):
    """Создает продукт в Stripe"""
    product = stripe.Product.create(
        name=course.title,
        description=course.description or 'Курс',
    )
    return product


def create_stripe_price(amount, product_id):
    """Создает цену в Stripe (сумма в копейках)"""
    price = stripe.Price.create(
        currency='rub',
        unit_amount=int(amount * 100),
        product=product_id,
    )
    return price


def create_stripe_session(price_id):
    """Создает сессию оплаты в Stripe и возвращает URL"""
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price': price_id,
            'quantity': 1,
        }],
        mode='payment',
        success_url='http://localhost:8000/success/',
        cancel_url='http://localhost:8000/cancel/',
    )
    return session


def get_stripe_session_status(session_id):
    """Получает статус сессии Stripe"""
    session = stripe.checkout.Session.retrieve(session_id)
    return session