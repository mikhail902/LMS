from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import PaymentViewSet

routers = DefaultRouter()
routers.register(r"payments", PaymentViewSet)

urlpatterns = [
    path("api/", include(routers.urls)),
]
urlpatterns += routers.urls
