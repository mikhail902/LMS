# courses/views.py
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, ListView, TemplateView
from rest_framework import viewsets, status
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from courses.tasks import send_course_update_email
from courses.models import Course, Lesson, Subscription
from courses.serializer import (CourseSerializer, LessonDetailSerializer,
                                LessonSerializer)
from courses.services import get_lesson_by_course
from courses.permissions import IsModerator, IsOwner
from .paginators import CourseLessonPagination
from users.models import Payment
from courses.serializer import PaymentSerializer
from courses.services import (
    create_stripe_product,
    create_stripe_price,
    create_stripe_session,
    get_stripe_session_status,
)


class MainView(TemplateView):
    template_name = "index.html"


class CoursesListView(LoginRequiredMixin, ListView):
    model = Course
    template_name = "courses_list.html"
    context_object_name = "courses"
    login_url = '/login/'


class CourseProductsListView(LoginRequiredMixin, DetailView):
    model = Course
    template_name = "lessons_list.html"
    login_url = '/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.get_object()
        lessons = get_lesson_by_course(category.id)
        context.update({"lessons": lessons})
        return context


class SingleLessonTemplateView(LoginRequiredMixin, DetailView):
    model = Lesson
    template_name = "single_lesson.html"
    context_object_name = "lessons"
    login_url = '/login/'


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CourseLessonPagination

    def perform_update(self, serializer):
        course = serializer.save()
        send_course_update_email.delay(course.id)

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsAuthenticated]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated, IsOwner | IsModerator]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Course.objects.none()
        user = self.request.user
        if user.groups.filter(name='moderators').exists():
            return Course.objects.all()
        return Course.objects.filter(author=user)


class LessonCreateApiView(CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class LessonListApiView(ListAPIView):
    serializer_class = LessonSerializer
    pagination_class = CourseLessonPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Lesson.objects.none()
        user = self.request.user
        if user.groups.filter(name='moderators').exists():
            return Lesson.objects.all()
        return Lesson.objects.filter(author=user)


class LessonRetrieveApiView(RetrieveAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        return LessonDetailSerializer

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Lesson.objects.none()
        user = self.request.user
        if user.groups.filter(name='moderators').exists():
            return Lesson.objects.all()
        return Lesson.objects.filter(author=user)


class LessonUpdateApiView(UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsOwner | IsModerator]


class LessonDestroyApiView(DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsOwner | IsModerator]


class ModeratorLessonListView(ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = CourseLessonPagination
    permission_classes = [IsAuthenticated, IsModerator]


class SubscriptionAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get('course_id')

        if not course_id:
            return Response(
                {'message': 'Не указан ID курса'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        course_item = get_object_or_404(Course, pk=course_id)
        subs_item = Subscription.objects.filter(user=user, course=course_item)

        if subs_item.exists():
            subs_item.delete()
            message = 'Подписка удалена'
        else:
            Subscription.objects.create(user=user, course=course_item)
            message = 'Подписка добавлена'

        return Response({'message': message})


class PaymentCreateAPIView(APIView):
    """Создание платежа и получение ссылки на оплату"""
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get('course_id')
        amount = request.data.get('amount')

        if not course_id or not amount:
            return Response(
                {'error': 'Не указан course_id или amount'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            course = Course.objects.get(pk=course_id)
        except Course.DoesNotExist:
            return Response(
                {'error': 'Курс не найден'},
                status=status.HTTP_404_NOT_FOUND,
            )

        try:
            product = create_stripe_product(course)
            price = create_stripe_price(float(amount), product.id)
            session = create_stripe_session(price.id)
        except Exception as e:
            return Response(
                {'error': f'Ошибка Stripe: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        payment = Payment.objects.create(
            user=user,
            paid_course=course,
            amount=amount,
            session_id=session.id,
            payment_url=session.url,
            payment_method='transfer',
        )

        serializer = PaymentSerializer(payment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PaymentStatusAPIView(APIView):
    """Проверка статуса платежа"""
    permission_classes = [IsAuthenticated]

    def get(self, request, payment_id):
        try:
            payment = Payment.objects.get(pk=payment_id, user=request.user)
        except Payment.DoesNotExist:
            return Response(
                {'error': 'Платеж не найден'},
                status=status.HTTP_404_NOT_FOUND,
            )

        if not payment.session_id:
            return Response(
                {'error': 'ID сессии не найден'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            session = get_stripe_session_status(payment.session_id)
        except Exception as e:
            return Response(
                {'error': f'Ошибка Stripe: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response({
            'payment_id': payment.id,
            'status': session.payment_status,
            'amount': str(payment.amount),
            'course': payment.paid_course.title if payment.paid_course else None,
        })