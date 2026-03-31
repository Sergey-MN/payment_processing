# payment_processing

Асинхронный микросервис для обработки платежей с гарантированной доставкой событий, поддержкой идемпотентности и
механизмом повторных попыток.

# Стек технологий

- **FastAPI** + Pydantic v2 — веб-фреймворк
- **SQLAlchemy 2.0** (асинхронный) — ORM
- **PostgreSQL** — основная БД
- **RabbitMQ** — брокер сообщений
- **Alembic** — миграции
- **Docker** + Docker Compose — контейнеризация

## Требования

- Docker и Docker Compose
- Git

## Настройка окружения

Перед запуском проекта необходимо создать файл `.env` в корневой директории проекта со следующими переменными окружения:

```bash
# PostgreSQL
POSTGRES_DB
POSTGRES_USER
POSTGRES_PASSWORD
POSTGRES_HOST
POSTGRES_PORT

# RabbitMQ
RABBITMQ_USER
RABBITMQ_PASSWORD
RABBITMQ_HOST
RABBITMQ_PORT
RABBITMQ_QUEUE=new
RABBITMQ_EXCHANGE=payments
RABBITMQ_MANAGEMENT_PORT
RABBITMQ_ROUTING_KEY=new

# API Security
API_KEY
```

## Быстрый старт

### 1. Клонирование репозитория

```bash
git clone https://github.com/Sergey-MN/payment_processing.git
cd payment_processing
```

### 2. Запуск сервиса

```bash
docker compose up --build -d
```

Эта команда запустит:

PostgreSQL

RabbitMQ (AMQP) и (Management UI)

Producer сервис

API сервис на порту 8000

Consumer сервис (обработчик платежей)

### 3. Остановка сервиса

```bash
docker compose down
```

## API Документация

После запуска сервиса интерактивная документация доступна по адресу:

Swagger UI: http://localhost:8000/docs

ReDoc: http://localhost:8000/redoc