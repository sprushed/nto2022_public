FROM python:3.9

WORKDIR /src
COPY requirements.txt /src

RUN apt-get update
RUN pip3 install --upgrade pip -r requirements.txt

COPY . /src
