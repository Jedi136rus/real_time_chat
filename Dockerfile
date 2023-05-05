FROM python:3

ENV FLASK_APP=sse_app
ENV REDIS_URL="redis://:password@redis:6379"

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

CMD ["python", "chat_db.py"]

CMD ["gunicorn", "sse_app:app", "--worker-class", "gevent", "--bind", "0.0.0.0:8000"]