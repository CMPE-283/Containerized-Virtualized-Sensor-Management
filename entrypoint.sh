#!/bin/bash
python manage.py migrate

echo Starting Gunicorn
exec gunicorn cvsms.wsgi:application \
    --name cvsms \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --log-level=info \
    "$@"
