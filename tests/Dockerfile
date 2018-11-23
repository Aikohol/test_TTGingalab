FROM python:3.6-alpine

MAINTAINER Brice PARENT <bparent@gingalab.com>

COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

#COPY src /
WORKDIR /src

CMD sh
# To launch the tests, execute this:
# dc run tests python -m unittest tests
