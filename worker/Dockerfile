FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
RUN pip install --no-cache-dir redis==5.2.1
COPY worker.py .
CMD ["python", "worker.py"]
