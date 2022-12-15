FROM python:3.8-buster

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

RUN apt update
RUN apt install socat -y

COPY ./CAESarism2.py /app/CAESarism2.py
COPY ./secret.py /app/secret.py

CMD socat TCP-L:17778,fork,reuseaddr EXEC:"python CAESarism2.py"
