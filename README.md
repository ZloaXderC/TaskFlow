# TaskFlow

TaskFlow — backend REST API для управления задачами.
Проект реализован на FastAPI с асинхронным SQLAlchemy и PostgreSQL.

В проекте реализованы JWT-аутентификация, refresh tokens,
разделение приложения на Router / Service / Repository,
проверка прав доступа и автоматические тесты.

## Стек

- Python
- FastAPI
- SQLAlchemy
- PostgreSQL
- Alembic
- JWT
- Pytest
- Docker

## Возможности

- Регистрация и авторизация пользователей
- JWT access tokens
- Refresh tokens
- Logout с отзывом refresh token
- CRUD задач
- Фильтрация задач
- Поиск
- Сортировка
- Пагинация
- Проверка прав доступа к задачам
- Валидация входных данных

## Архитектура


Router → Service → Repository → PostgreSQL

## Структура проекта

app/
├── core/
├── db/
├── models/
├── schemas/
├── repositories/
├── service/
├── dependecies/
├── routers/
└── main.py

tests/
├── conftest.py
└── test_main.py

### API

### Auth

POST /auth/register
POST /auth/login
POST /auth/refresh
POST /auth/logout

### Tasks

POST /task
GET /task
GET /task/{task_id}
PATCH /task/{task_id}
DELETE /task/{task_id}

## Документация API

Swagger:

http://localhost:8000/docs

## Тестирование

Команда:

python -m pytest -v

Тестами покрыты:

- authentication
- CRUD
- permissions
- validation
- filtering
- search
- refresh/logout

## Миграции

alembic upgrade head
