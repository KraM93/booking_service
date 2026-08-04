# 🎟️ Seat Booking API Service

![Python](https://img.shields.io/badge/python-3.12-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688.svg?style=flat&logo=FastAPI&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791.svg?style=flat&logo=postgresql&logoColor=white)
![Alembic](https://img.shields.io/badge/Alembic-Migrations-red.svg)
![CI/CD](https://img.shields.io/badge/GitHub%20Actions-CI%2FCD-2088FF.svg?logo=github-actions&logoColor=white)
![Coverage](https://img.shields.io/badge/coverage-81%25-brightgreen.svg)

Асинхронный RESTful API сервис для бронирования мест на мероприятия. Проект спроектирован с учётом лучших практик бэкенд-разработки: полная асинхронность, надёжная аутентификация, защита от спама, автоматическое тестирование и CI/CD пайплайн.

---

## 🌟 Ключевые особенности

- **Асинхронное ядро**: Построено на `FastAPI` + `SQLAlchemy 2.0 (AsyncSession)` + `asyncpg`.
- **Безопасность и Аутентификация**: 
  - Регистрация и аутентификация пользователей с использованием JWT-токенов (`OAuth2PasswordBearer`).
  - Безопасное хэширование паролей через `Passlib` (`bcrypt`).
- **Защита от спама и брутфорса**: Интеграция `SlowAPI` для ограничений количества запросов (Rate Limiting) на критических эндпоинтах.
- **Асинхронное логирование**: Неблокирующая система логов на базе `Loguru` с ротацией файлов и асинхронной очередью (`enqueue=True`).
- **Управление базой данных**: Автоматические миграции схемы БД через `Alembic`.
- **Надёжность и Тестирование**: 
  - Набор автотестов с асинхронным HTTP-клиентом (`pytest` + `pytest-asyncio` + `httpx`).
  - **81% честного покрытия** чистого бизнес-кода (`pytest-cov`).
- **CI/CD Автоматизация**: Автоматический запуск тестирования в GitHub Actions при каждом `push` в ветку `main`.
- **Контейнеризация**: Готовые конфигурации `Dockerfile` и `docker-compose.yml` для развёртывания приложения в связке с PostgreSQL.

---

## 🛠️ Технологический стек

- **Language**: Python 3.12
- **Framework**: FastAPI
- **Database & ORM**: PostgreSQL, SQLAlchemy (Async), asyncpg
- **DB Migrations**: Alembic
- **Validation & Settings**: Pydantic v2, `pydantic-settings`
- **Security**: PyJWT, Passlib (Bcrypt)
- **Rate Limiting**: SlowAPI
- **Logging**: Loguru
- **Testing**: Pytest, Pytest-Asyncio, Pytest-Cov, HTTPX
- **DevOps & CI/CD**: Docker, Docker Compose, GitHub Actions

---

## 📁 Структура проекта

```text
booking_service/
├── .github/workflows/   # CI/CD автотесты для GitHub Actions
│   └── tests.yml
├── alembic/             # Скрипты и история миграций базы данных
├── logs/                # Логи приложения (автоматическая ротация)
├── routers/             # Эндпоинты API
│   ├── events.py        # Управление мероприятиями
│   ├── seats.py         # Просмотр и бронирование мест
│   └── users.py         # Регистрация и авторизация
├── tests/               # Модульные и интеграционные автотесты
│   ├── test_auth.py
│   ├── test_booking.py
│   └── test_crud.py
├── .env.example         # Пример конфигурации переменных окружения
├── .gitignore
├── config.py            # Валидация настроек через Pydantic Settings
├── conftest.py          # Фикстуры pytest и тестовая БД в памяти
├── crud.py              # Слой работы с базой данных (CRUD)
├── database.py          # Настройка AsyncEngine и сессий SQLAlchemy
├── Dockerfile           # Инструкция сборки Docker-образа
├── docker-compose.yml   # Запуск приложения и PostgreSQL в контейнерах
├── limiter.py           # Конфигурация SlowAPI (Rate Limiter)
├── logger.py            # Настройка асинхронного логгера Loguru
├── main.py              # Точка входа FastAPI приложения
├── models.py            # SQLAlchemy модели (Users, Events, Seats)
├── pytest.ini           # Настройки pytest и отчётов покрытия
├── requirements.txt     # Зависимости проекта
├── schemas.py           # Pydantic схемы валидации
└── security.py          # Хэширование паролей и работа с JWT
```

---

## 🚀 Быстрый запуск

### 1. Клонирование репозитория

```bash 
git clone https://github.com/KraM93/booking_service.git
cd booking_service
```

### 2. Настройка переменных окружения

Создайте файл .env в корне проекта:

```env
DATABASE_URL=postgresql+asyncpg://postgres:postgrespassword@localhost:5432/booking_db
SECRET_KEY=super_secret_jwt_key_change_me_in_production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 3. Запуск локально
#### 3.1 Создайте и активируйте виртуальное окружение:

```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate
```

#### 3.2 Установите зависимости:

```bash
pip install -r requirements.txt
```

#### 3.3 Примените миграции базы данных:

```bash
alembic upgrade head
```

#### 3.4 Запустите сервер разработки:

```bash
uvicorn main:app --reload
```

Сервер будет доступен по адресу: `http://127.0.0.1:8000`

---

## 🐳 Запуск через Docker Compose

Для запуска приложения вместе с базой данных PostgreSQL в контейнерах:

```bash
docker-compose up --build
```

Применение миграций внутри запущенного контейнера:

```bash
docker-compose exec web alembic upgrade head
```
---

## 🧪 Тестирование и Покрытие (Coverage)

Запуск всех автотестов с выводом отчета по покрытию кода:

```bash
pytest
```

Метрики покрытия бизнес-логики:

- Общее покрытие: **81%**
- Автоматический прогон тестов при каждом `git push` через **GitHub Actions**.

## 📖 Документация API

После запуска сервера документация API доступна в интерактивных форматах:

- **Swagger UI**: `http://127.0.0.1:8000/docs`
- **ReDoc**: `http://127.0.0.1:8000/redoc`
