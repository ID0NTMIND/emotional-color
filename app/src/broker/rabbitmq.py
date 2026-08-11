import pika
import json
import os


RABBITMQ_URL = os.getenv("RABBITMQ_URL", "amqp://guest:guest@rabbitmq:5672/")


def get_connection() -> pika.BlockingConnection:
    params = pika.URLParameters(RABBITMQ_URL)
    return pika.BlockingConnection(params)


def publish_task(task_id: str) -> None:
    connection = get_connection()
    channel = connection.channel()
    channel.queue_declare(queue='ml_tasks', durable=True)

    message = json.dumps({"task_id": task_id})
    channel.basic_publish(
        exchange='',
        routing_key='ml_tasks',
        body=message,
        properties=pika.BasicProperties(delivery_mode=2)
    )
    connection.close()
