#!/bin/sh

cd /var/app/current && python manage.py migrate --noinput
supervisord -n -c /etc/supervisor/supervisord.conf