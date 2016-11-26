FROM python:3.5
MAINTAINER @dimmg <dumitru.gira@gmail.com>

ENV APP_PATH /usr/src/app

RUN mkdir -p $APP_PATH
WORKDIR $APP_PATH/core

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .
