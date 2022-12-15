#FROM ubuntu:22.04
FROM archlinux:latest

#RUN apt-get update && apt-get install socat sudo -yqq
RUN pacman -Sy && pacman -S socat sudo --noconfirm

WORKDIR /task

COPY ./flag.txt ./
COPY ./server.sh /
COPY skyfall libc.so.6 ld.so ./

EXPOSE 1337
ENTRYPOINT /server.sh
