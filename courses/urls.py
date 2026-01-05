from django.urls import path

from . import views
from .apps import CoursesConfig

app_name = CoursesConfig.name

urlpatterns = [
    path("test/", views.MainView.as_view(), name="index"),
    path("", views.CoursesListView.as_view(), name="courses_list"),
    path(
        "course/<int:pk>/", views.CourseProductsListView.as_view(), name="lessons_list"
    ),
    path("lesson/<int:pk>/", views.SingleLessonTemplateView.as_view(), name="lesson"),
]
