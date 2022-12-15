FROM ubuntu:22.04

RUN apt-get update && apt-get install socat sudo -yqq
WORKDIR /task

#RUN pacman -Sy && pacman -S socat sudo --noconfirm

COPY ./flag.txt ./
COPY ./server.sh /
COPY shock libc.so.6 ld.so ./

EXPOSE 1337
ENTRYPOINT /server.sh
