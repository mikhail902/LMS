from django.urls import path
from rest_framework.routers import SimpleRouter

from .apps import CoursesConfig
from .views import (CourseViewSet, LessonCreateApiView, LessonDestroyApiView,
                    LessonListApiView, LessonRetrieveApiView,
                    LessonUpdateApiView)

app_name = CoursesConfig.name

routers = SimpleRouter()
routers.register("", CourseViewSet)

urlpatterns = [
    # path("test/", views.MainView.as_view(), name="index"),
    # path("", views.CoursesListView.as_view(), name="courses_list"),
    # path("course/<int:pk>/", views.CourseProductsListView.as_view(), name="lessons_list"),
    # path("lesson/<int:pk>/", views.SingleLessonTemplateView.as_view(), name="lesson"),
    path("lessons", LessonListApiView.as_view(), name="lesson_list"),
    path("lessons/<int:pk>", LessonRetrieveApiView.as_view(), name="lesson_retrieve"),
    path("lessons/create", LessonCreateApiView.as_view(), name="lesson_Create"),
    path(
        "lessons/<int:pk>/delete", LessonDestroyApiView.as_view(), name="lesson_delete"
    ),
    path(
        "lessons/<int:pk>/update", LessonUpdateApiView.as_view(), name="lesson_update"
    ),
]
urlpatterns += routers.urls
