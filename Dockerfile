FROM ubuntu:20.04
ENV LANGUAGE ru_RU.UTF-8
ENV LANG ru_RU.UTF-8
ENV LC_ALL ru_RU.UTF-8
ENV TZ=Europe/Moscow
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

MAINTAINER Peter Chaikin 'chay-ka2008@yandex.ru'

RUN apt-get -y update && apt-get -y upgrade && apt-get install -y  \
    && apt-get install -y curl python3-pip

ENV FLASK_APP=sse_app
ENV REDIS_URL="redis://redis_chat:6379"

COPY . /app

WORKDIR /app

RUN pip install -r requirements.txt

CMD ["python", "chat_db.py"]