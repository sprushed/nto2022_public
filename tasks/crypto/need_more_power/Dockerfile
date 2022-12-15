FROM python:3.8-buster

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

RUN apt update
RUN apt install socat -y

COPY ./need_more_power.py /app/need_more_power.py
COPY ./params.py /app/params.py

CMD socat TCP-L:18181,fork,reuseaddr EXEC:"python need_more_power.py"
