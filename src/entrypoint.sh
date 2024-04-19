#!/bin/sh

echo "$CRON_SCHEDULE /opt/sync_files.py  > /tmp/sync.log 2>&1" > ~/cronjob

crontab ~/cronjob

/usr/sbin/crond -f -d 5
