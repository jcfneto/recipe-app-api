FROM python:3.7-alpine
MAINTAINER Jose Carlos Ferreira Neto

# builds python withou buffer mode
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
RUN pip install -r requirements.txt

RUN mkdir /app
WORKDIR /app
COPY ./app /app

RUN adduser -D user
USER user