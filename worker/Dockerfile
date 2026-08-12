FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir torch==2.13.0+cpu --index-url https://download.pytorch.org/whl/cpu

COPY src/ ./src/

ENV PYTHONPATH=/app

CMD ["python", "-u", "src/worker.py"]