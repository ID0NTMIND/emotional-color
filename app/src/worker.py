from src.domain_model import TextSentimentModel
from src.db.models import MLTask, MLModel, PredictionResult, TaskStatus
from src.db.database import engine
import json
import os
import sys
import time
import random
import pika
from decimal import Decimal
from sqlmodel import Session, select

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

RABBITMQ_URL = os.getenv("RABBITMQ_URL", "amqp://guest:guest@rabbitmq:5672/")
WORKER_ID = os.getenv("WORKER_ID", f"worker-{random.randint(1,100)}")


def process_task(task_id: str):
    """Обрабатывает одну ML-задачу"""
    with Session(engine) as session:
        task = session.get(MLTask, task_id)
        if not task:
            print(f"[{WORKER_ID}] Task {task_id} not found")
            return

        if task.status != TaskStatus.PENDING:
            print(
                f"[{WORKER_ID}] Task {task_id} already processed (status={task.status})")
            return

        model = session.exec(select(MLModel).where(
            MLModel.id == task.model_id)).first()
        if not model:
            task.status = TaskStatus.FAILED
            session.add(task)
            session.commit()
            print(f"[{WORKER_ID}] Model not found for task {task_id}")
            return

        sentiment_model = TextSentimentModel()
        prediction_result = sentiment_model.predict(task.input_data)

        result = PredictionResult(
            task_id=task.id,
            label=prediction_result.label,
            confidence=prediction_result.confidence,
            model_id=model.id,
        )
        session.add(result)
        task.status = TaskStatus.COMPLETED
        session.add(task)
        session.commit()
        print(f"[{WORKER_ID}] Task {task_id} completed: {prediction_result.label} ({prediction_result.confidence})")


def callback(ch, method, properties, body):
    """Функция, вызываемая при получении сообщения из очереди"""
    data = json.loads(body)
    task_id = data.get("task_id")
    print(f"[{WORKER_ID}] Received task {task_id}")
    try:
        process_task(task_id)
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        print(f"[{WORKER_ID}] Error processing task {task_id}: {e}")
        ch.basic_nack(delivery_tag=method.delivery_tag)


def main():
    params = pika.URLParameters(RABBITMQ_URL)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    channel.queue_declare(queue='ml_tasks', durable=True)
    channel.basic_qos(prefetch_count=1)  # за раз берём не больше одной задачи
    channel.basic_consume(queue='ml_tasks', on_message_callback=callback)

    print(f"[{WORKER_ID}] Started. Waiting for tasks...")
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        channel.stop_consuming()
    connection.close()


if __name__ == "__main__":
    main()
