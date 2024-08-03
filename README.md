# TestWebTask

TestWebTask - это веб-приложение, написанное на FastAPI, с базой данных MongoDB и веб-сервером Nginx. Также в проекте используется Telegram бот, который показывает сообщения и позволяет создавать новые сообщения.

## Структура проекта

```
TestWebTask/
│
├── app/
│   ├── main.py
│   ├── Dockerfile
│   ├── requirements.txt
│
├── bot/
│   ├── bot.py
│   ├── Dockerfile
│   ├── requirements.txt
│
├── nginx/
│   ├── nginx.conf
│
├── .env
├── docker-compose.yml
└── README.md
```

## Требования

- Docker
- Docker Compose

## Установка

1. Склонируйте репозиторий:

```bash
git clone https://github.com/your-username/TestWebTask.git
cd TestWebTask
```

2. Создайте файл `.env` в корне проекта и добавьте следующие переменные окружения:

```
MONGO_URI=mongodb://mongo:27017
DB_NAME=db_name
COLLECTION=collection_name
BOT_TOKEN=your_bot_token
```

## Запуск

Запустите Docker Compose для сборки и запуска всех контейнеров:

```bash
docker-compose up --build
```

## Эндпоинты FastAPI

- **GET** `/api/v1/messages/` - Получить список всех сообщений.
- **POST** `/api/v1/message/` - Создать новое сообщение. Пример запроса:
  ```json
  {
    "content": "Hello, world!"
  }
  ```

## Использование Telegram бота

1. Откройте Telegram и найдите вашего бота по имени.
2. Отправьте команду `/start` или `/help` для начала работы.
3. Отправьте сообщение боту, чтобы сохранить его в базе данных.

## Конфигурация Nginx

Файл конфигурации Nginx находится в `nginx/nginx.conf`. Он настроен для проксирования запросов к FastAPI приложению:

```nginx
worker_processes 1;

events {
    worker_connections 1024;
}

http {
    server {
        listen 80;
        server_name localhost;

        location / {
            proxy_pass http://app:8000;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }
}
```
