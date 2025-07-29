# habits_course_work

Проект реализовывает трекер привычек. Пользователь имеет возможность записывать свои привычки, напоминание о которых
происходит путем рассылки через телеграм бота

## 🛠 Технологии
- Python 3.11
- Django 5.5.0
- PostgreSQL
- Docker + Docker Compose

## 🚀 Запуск проекта

### Локальная разработка (с Docker)

1. Склонируйте репозиторий:
   ```bash
   git clone git@github.com:Dal-Opez/diplom_bulletin_board.git
   ```
2. Создайте файл .env в корне проекта (пример в .env.example):
   ```
    SECRET_KEY=<ваш-secret-key>
    NAME=<имя-бд>
    USER=<пользователь-бд>
    PASSWORD=<пароль-бд>
    # Остальные переменные...
   ```
3. Запустите сервисы:
```
docker-compose up -d --build
```
4. Примените миграции:
```
docker-compose exec web python manage.py migrate
```

5. Проект доступен по адресу:
```
http://localhost:8000
```

### Тестирование
1. Для запуска тестов выполните:
   ```bash
   pytest -v
   ```

2. Для проведения тестов с подробным отчетом, сформированном в html файле выполните:
   ```bash
   pytest --cov=users --cov-report=html -v   
   ```