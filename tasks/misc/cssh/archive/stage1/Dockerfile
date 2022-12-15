# Chmod chmod
FROM containerssh/agent AS agent

FROM debian
COPY --from=agent /usr/bin/containerssh-agent /usr/bin/containerssh-agent

RUN useradd -m user

RUN apt update && apt install -y lsof inotify-tools procps supervisor vim sudo
RUN mkdir -p /var/log/supervisor
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
COPY processes /root/processes/
RUN chmod o-r -R /root/processes/

RUN echo "export TERM=xterm-256color" >> /home/user/.bashrc
RUN echo "echo '======================================================================================================================================'" >> /home/user/.bashrc
RUN echo "echo 'One of the processes on these machine is constantly using the file /tmp/weird. The name of the process is the password to next stage!'" >> /home/user/.bashrc
RUN echo "echo '======================================================================================================================================'" >> /home/user/.bashrc
RUN echo "sudo /usr/bin/supervisord -c /etc/supervisor/supervisord.conf" >> /home/user/.bashrc
COPY ./sudoers /etc/sudoers
RUN chmod 440 /etc/sudoers

USER user
WORKDIR /home/user
