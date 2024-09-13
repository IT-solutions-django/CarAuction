# Django CarAuction

### Основные функции:
- Просмотр списка автомобилей + пагинация
- Просмотр списка автомобилей через фильтрацию
- REST API для работы с автомобилями 

## Стек технологий

- Python (3.x)
- Django 
- Django REST Framework (DRF)
- PostgreSQL 

## Установка и запуск

### Шаги установки

1. Клонируйте репозиторий на локальную машину:

   ```bash
   git clone https://github.com/IT-solutions-django/CarAuction.git
   ```
   Перейдите в каталог
2. Запустите проект с помощью Docker Compose:

   ```bash
   docker-compose up --build
   ```
3. Выполните миграции внутри контейнера:

   ```bash
   docker-compose exec web python manage.py migrate
   ```
