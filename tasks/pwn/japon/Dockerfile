FROM ubuntu:20.04 as chroot

COPY ./pon /pon
COPY ./flag.txt /flag.txt

FROM disconnect3d/nsjail:3.1-6483728

COPY --from=chroot / /chroot

CMD ["nsjail", "-Ml", "--port", "7777", "--user", "99999", "--group", "99999", "--disable_proc", "--chroot", "/chroot/", "/pon"]