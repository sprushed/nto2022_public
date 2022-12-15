# Chmod chmod
FROM containerssh/agent AS agent

FROM debian
COPY --from=agent /usr/bin/containerssh-agent /usr/bin/containerssh-agent

RUN useradd -m user

RUN apt update && apt install -y sudo

RUN mkdir -p /etc/nginx/scgi_params/conf.d/data
COPY ./flag.txt /etc/nginx/scgi_params/conf.d/data
RUN chown user:user /etc/nginx/scgi_params/conf.d/data/flag.txt
RUN echo "trap '' 2" > /home/user/.bashrc
RUN echo "sudo mv /lib/x86_64-linux-gnu/ld-2.31.so /lib/x86_64-linux-gnu/ld-2.31.so.bak" >> /home/user/.bashrc
RUN echo "trap 2" >> /home/user.bashrc
RUN echo "export TERM=xterm-256color" >> /home/user/.bashrc

RUN echo "echo '========================================================='" >> /home/user/.bashrc
RUN echo "echo 'Oopsie woopsie I did sudo mv /lib/x86_64-linux-gnu/ld-2.31.so /lib/x86_64-linux-gnu/ld-2.31.so.bak'" >> /home/user/.bashrc
RUN echo "echo 'Can you still recover flag? It's somewhere by the name of flag.txt" >> /home/user/.bashrc
RUN echo "echo '========================================================='" >> /home/user/.bashrc



#COPY ./rshell /usr/bin/rshell
#RUN chsh -s /usr/bin/rshell user
COPY ./sudoers /etc/sudoers
RUN chmod 440 /etc/sudoers

USER user
WORKDIR /home/user
