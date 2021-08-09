# syntax=docker/dockerfile:1
FROM python:3
ENV PYTHONUNBUFFERED=1
COPY .aws /root/.aws
WORKDIR /code
COPY iot_camera_server/requirements.txt /code/iot_camera_server
RUN pip install -r iot_camera_server/requirements.txt
COPY . /code/