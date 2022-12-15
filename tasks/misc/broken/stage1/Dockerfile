# Chmod chmod
FROM golang:1.19 as build

COPY flagprinter.go /go/src/app/
RUN CGO_ENABLED=0 go build -o /go/bin/flagprinter /go/src/app/flagprinter.go 
RUN dd if=/dev/zero of=zeros bs=10M count=5
RUN cat zeros >> /go/bin/flagprinter

FROM containerssh/agent AS agent

FROM debian
COPY --from=agent /usr/bin/containerssh-agent /usr/bin/containerssh-agent

RUN useradd -m user

COPY --from=build /go/bin/flagprinter /home/user
RUN chmod -xrw /home/user/flagprinter
RUN chown user /home/user/flagprinter
RUN echo "export TERM=xterm-256color" >> /home/user/.bashrc

RUN echo "echo '==================================================================================='" >> /home/user/.bashrc
RUN echo "echo 'flagprinter will output flag on execution, but chmod is -x...'" >> /home/user/.bashrc
RUN echo "echo '==================================================================================='" >> /home/user/.bashrc


RUN apt remove -y perl && apt autoremove -y && rm /usr/bin/perl && rm /usr/bin/perl5.32.1
RUN chmod -x /bin/chmod
RUN rm /bin/cp
RUN rm /bin/tar

USER user
WORKDIR /home/user
