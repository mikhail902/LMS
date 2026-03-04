from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import PaymentViewSet, UserCreateApiView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

routers = DefaultRouter()
routers.register(r"payments", PaymentViewSet)

urlpatterns = [
    path("api/", include(routers.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register', UserCreateApiView.as_view(), name='register'),
]
urlpatterns += routers.urls
