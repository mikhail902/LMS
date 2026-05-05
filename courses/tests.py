from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

from .models import Course, Lesson, Subscription

User = get_user_model()


class LessonTestCase(APITestCase):
    """Тесты CRUD уроков"""

    def setUp(self):
        self.user = User.objects.create_user(
            email='test@test.ru',
            password='testpass123'
        )
        self.course = Course.objects.create(
            title='Test Course',
            description='Test Description'
        )
        self.lesson = Lesson.objects.create(
            title='Test Lesson',
            description='Test Lesson Description',
            course=self.course,
            video_url='https://www.youtube.com/watch?v=test'
        )
        self.client.force_authenticate(user=self.user)

    def test_create_lesson_valid_link(self):
        """Создание урока с YouTube-ссылкой"""
        data = {
            'title': 'New Lesson',
            'description': 'New Description',
            'course': self.course.id,
            'video_url': 'https://www.youtube.com/watch?v=new'
        }
        response = self.client.post('/lessons/create', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_lesson_invalid_link(self):
        """Создание урока с запрещенной ссылкой"""
        data = {
            'title': 'Bad Lesson',
            'description': 'Bad Description',
            'course': self.course.id,
            'video_url': 'https://www.google.com'
        }
        response = self.client.post('/lessons/create', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_lessons_list(self):
        """Получение списка уроков"""
        response = self.client.get('/lessons')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_lesson(self):
        """Обновление урока"""
        data = {'title': 'Updated Lesson'}
        response = self.client.patch(
            f'/lessons/{self.lesson.id}/update', data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_lesson(self):
        """Удаление урока"""
        response = self.client.delete(
            f'/lessons/{self.lesson.id}/delete'
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class SubscriptionTestCase(APITestCase):
    """Тесты подписки на курс"""

    def setUp(self):
        self.user = User.objects.create_user(
            email='test@test.ru',
            password='testpass123'
        )
        self.course = Course.objects.create(
            title='Test Course',
            description='Test Description'
        )
        self.client.force_authenticate(user=self.user)

    def test_subscribe(self):
        """Подписка на курс"""
        data = {'course_id': self.course.id}
        response = self.client.post('/subscription/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Подписка добавлена')

    def test_unsubscribe(self):
        """Отписка от курса"""
        Subscription.objects.create(user=self.user, course=self.course)
        data = {'course_id': self.course.id}
        response = self.client.post('/subscription/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Подписка удалена')

    def test_course_shows_subscription_status(self):
        """Курс показывает признак подписки"""
        Subscription.objects.create(user=self.user, course=self.course)
        response = self.client.get(f'/{self.course.id}/')
        self.assertTrue(response.data['is_subscribed'])