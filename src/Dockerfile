FROM alpine:latest

ARG USER=rclone

RUN apk update
RUN apk add --no-cache rclone python3 dcron libcap

RUN addgroup $USER
RUN adduser -D  -G $USER $USER

RUN mkdir /opt/sync
RUN chown $USER:$USER /opt/sync

RUN chown $USER:$USER /usr/sbin/crond
RUN setcap cap_setgid=ep /usr/sbin/crond

RUN chown $USER:$USER /usr/bin/crontab
RUN setcap cap_setgid=ep /usr/bin/crontab

RUN chown -R $USER:$USER /etc/crontabs

COPY sync_files.py /opt/
RUN chmod +x /opt/sync_files.py

COPY --chown=$USER:$USER entrypoint.sh /home/$USER/entrypoint.sh

USER $USER

WORKDIR /home/$USER
ENTRYPOINT ["./entrypoint.sh"]
