from django.shortcuts import render
from django.views.generic import DetailView, ListView, TemplateView
from rest_framework.viewsets import ModelViewSet
from courses.models import Course, Lesson
from courses.services import get_lesson_by_course
from courses.serializer import LessonSerializer, CourseSerializer
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
class MainView(TemplateView):
    template_name = "index.html"


class CoursesListView(ListView):
    """CBV для списка продуктов"""

    model = Course
    template_name = "courses_list.html"
    context_object_name = "courses"


class CourseProductsListView(DetailView):
    model = Course
    template_name = "lessons_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.get_object()
        lessons = get_lesson_by_course(category.id)
        context.update(
            {
                "lessons": lessons,
            }
        )
        return context


class SingleLessonTemplateView(DetailView):
    model = Lesson
    template_name = "single_lesson.html"
    context_object_name = "lessons"

class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

class LessonCreateApiView(CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

class LessonListApiView(ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

class LessonRetrieveApiView(RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

class LessonUpdateApiView(UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

class LessonDestroyApiView(DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer