# Sentiment ML Service

Сервис анализа тональности текста (positive / neutral / negative) с REST API, веб-интерфейсом, RabbitMQ и ML-моделью.

## Возможности

- Регистрация и авторизация (Bearer-токен)
- Баланс пользователя и его пополнение
- Отправка текста на анализ, списание кредитов
- Асинхронная обработка задач воркерами
- История транзакций и предсказаний
- Web-интерфейс

## Стек

- **Backend:** FastAPI, SQLModel, PostgreSQL
- **Broker:** RabbitMQ
- **ML:** Hugging Face Transformers (DistilBERT multilingual sentiment)
- **Frontend:** Jinja2, HTML, CSS, JS
- **Инфраструктура:** Docker, Docker Compose, Nginx
- **Тесты:** pytest + requests

## Запуск

```bash
docker compose up --build
```

## Запуск

- Веб-интерфейс: http://localhost/

- Swagger API: http://localhost/docs

- RabbitMQ Management: http://localhost:15672 (guest/guest)
