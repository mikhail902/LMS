from django_filters import rest_framework as filters
from rest_framework import permissions, viewsets
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated

from .filters import PaymentFilter
from .models import Payment, User
from .serializers import PaymentSerializer, UserSerializer


class PaymentViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с платежами.
    """

    queryset = Payment.objects.all().select_related(
        "user", "paid_course", "paid_lesson"
    )
    serializer_class = PaymentSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = PaymentFilter
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Для обычных пользователей показываем только их платежи.
        Для админов - все платежи.
        """
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            queryset = queryset.filter(user=self.request.user)

        return queryset

    def perform_create(self, serializer):
        """Автоматически привязываем текущего пользователя к платежу"""
        serializer.save(user=self.request.user)

class UserCreateApiView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        user.set_password(user.password)
        user.save()