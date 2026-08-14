# 📚 Платформа для онлайн-обучения (LMS) — Backend

Серверная часть платформы для онлайн-обучения, предоставляющая REST API для создания, управления и прохождения онлайн-курсов. Система предназначена для интеграции с SPA-приложениями и возвращает клиенту структурированные JSON-данные.

---

## 🚀 Особенности

- ✅ Полноценная система управления курсами с модулями и уроками
- ✅ Ролевая модель пользователей (студенты, преподаватели, администраторы)
- ✅ Отслеживание прогресса обучения
- ✅ Система проверки знаний (тесты, задания)
- ✅ Обсуждения и отзывы о курсах
- ✅ REST API с JWT-аутентификацией
- ✅ Полная документация API (Swagger / ReDoc)
- ✅ Асинхронная обработка задач (Celery + Redis)
- ✅ Периодические задачи (Celery Beat)
- ✅ Интеграция с платёжной системой Stripe
- ✅ Рассылка уведомлений по email
- ✅ Валидация внешних ссылок
- ✅ Пагинация
- ✅ CORS

---

## 🛠 Стек технологий

| Технология | Назначение |
|------------|------------|
| **Python 3.10+** | Язык программирования |
| **Django** | Веб-фреймворк |
| **Django REST Framework** | REST API |
| **PostgreSQL** | База данных |
| **Redis** | Брокер сообщений |
| **Celery** | Асинхронная очередь задач |
| **Celery Beat** | Периодические задачи |
| **Stripe** | Платёжная система |
| **JWT (Simple JWT)** | Аутентификация |
| **drf-yasg** | Документация API (Swagger / ReDoc) |
| **django-cors-headers** | CORS |
| **django-filter** | Фильтрация |
| **django-celery-beat** | Хранение расписаний в БД |
| **eventlet** | Асинхронность для Windows |

---

## 📦 Установка и настройка

# 1. Клонировать репозиторий
git clone https://github.com/mikhail902/LMS.git
cd LMS

# 2. Скопировать .env файл
cp .env.template .env
# Заполнить .env своими значениями

# 3. Установить зависимости
poetry install

# 4. Применить миграции
poetry run python manage.py migrate

# 5. Запустить сервер
poetry run python manage.py runserver

______________________________________________________

# 1. Запустить все сервисы
docker-compose -f docker/docker-compose.yml up -d

# 2. Применить миграции
docker-compose -f docker/docker-compose.yml exec web python manage.py migrate

# 3. Создать суперпользователя
docker-compose -f docker/docker-compose.yml exec web python manage.py createsuperuser

# 4. Остановить все сервисы
docker-compose -f docker/docker-compose.yml down

______________________________________________________

# 1. Установка Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# 2. Установка Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# 3. Создание директории проекта
sudo mkdir -p /opt/drf-app
sudo chown $USER:$USER /opt/drf-app

# 4. Копирование .env файла
cp .env.template /opt/drf-app/.env
# Заполнить .env реальными значениями

# 5. Запуск
cd /opt/drf-app
docker-compose -f docker/docker-compose.prod.yml up -d

# 6. Проверка статуса
docker-compose -f docker/docker-compose.prod.yml ps
docker-compose -f docker/docker-compose.prod.yml logs -f