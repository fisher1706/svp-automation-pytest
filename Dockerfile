FROM python:3.10-alpine

COPY requirements.txt /

RUN \
    apk update && apk add --no-cache curl jq git bash g++ gcc linux-headers libffi-dev && \
    pip3 install --upgrade pip setuptools && \
    pip3 install --no-cache-dir  --force-reinstall -Iv grpcio==1.40 && \
    pip3 install -r /requirements.txt

COPY . /app

COPY . /opt/src/svp-automation

WORKDIR /app
