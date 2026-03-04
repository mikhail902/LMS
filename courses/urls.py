from django.urls import path
from rest_framework.routers import SimpleRouter

from .apps import CoursesConfig
from .views import (CourseViewSet, LessonCreateApiView, LessonDestroyApiView,
                    LessonListApiView, LessonRetrieveApiView,
                    LessonUpdateApiView, ModeratorLessonListView)

app_name = CoursesConfig.name

routers = SimpleRouter()
routers.register("", CourseViewSet)

urlpatterns = [
    path("lessons", LessonListApiView.as_view(), name="lesson_list"),
    path("lessons/<int:pk>", LessonRetrieveApiView.as_view(), name="lesson_retrieve"),
    path("lessons/create", LessonCreateApiView.as_view(), name="lesson_create"),
    path("lessons/<int:pk>/delete", LessonDestroyApiView.as_view(), name="lesson_delete"),
    path("lessons/<int:pk>/update", LessonUpdateApiView.as_view(), name="lesson_update"),
    path('moderator/lessons/', ModeratorLessonListView.as_view(), name='moderator-lessons'),
]

urlpatterns += routers.urls