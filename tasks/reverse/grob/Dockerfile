FROM archlinux:base-20221127.0.105785
COPY hashcash-1.22-5-x86_64.pkg.tar.zst /tmp/
RUN pacman -Syyu --noconfirm qemu-system-x86 socat
RUN pacman -U --noconfirm /tmp/hashcash-1.22-5-x86_64.pkg.tar.zst; rm /tmp/hashcash-1.22-5-x86_64.pkg.tar.zst
RUN mkdir /chal
COPY boot_prod.img run.sh hashcashed listen.sh /chal/
RUN chmod 555 /chal/run.sh /chal/hashcashed /chal/listen.sh; chmod 444 /chal/boot_prod.img
USER nobody
ENTRYPOINT ["/chal/listen.sh"]

