FROM python:3.6-alpine

MAINTAINER Brice PARENT <bparent@gingalab.com>

EXPOSE 8123

COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

WORKDIR /src

CMD gunicorn --reload --bind=0.0.0.0:8123 main:__hug_wsgi__
