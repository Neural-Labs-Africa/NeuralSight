FROM python:3.9-slim

WORKDIR /app/
# RUN apt-get update && apt-get install -y python3-opencv
RUN apt-get update && apt-get install libgl1 -y
COPY ./requirements.txt /tmp/requirements.txt
RUN pip3 install -r /tmp/requirements.txt
COPY . /app/
ENV PYTHONPATH=/app