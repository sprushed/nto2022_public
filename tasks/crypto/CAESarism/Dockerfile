FROM python:3.8-buster

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

RUN apt update
RUN apt install socat -y

COPY ./CAESarism.py /app/CAESarism.py
COPY ./secret.py /app/secret.py

CMD socat TCP-L:17777,fork,reuseaddr EXEC:"python CAESarism.py"
