FROM python:3
ENV PYTHONUNBUFFERED 1

RUN apt-get update \
    && apt-get install -y sqlite3 libsqlite3-dev

RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/

RUN pip install -r requirements.txt
COPY . /code/