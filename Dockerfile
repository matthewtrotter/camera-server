# syntax=docker/dockerfile:1
FROM python:3
ENV PYTHONUNBUFFERED=1
COPY .aws /root/.aws
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/