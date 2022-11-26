#!/usr/bin/env bash
# set -o nounset

python djlodging/django_app/manage.py collectstatic --noinput
# python djlodging/django_app/manage.py migrate
# nginx
# nginx -g "daemon off;"

(gunicorn --bind 0.0.0.0:8010 djlodging.django_app.django_core.wsgi --workers 3) & nginx -g "daemon off;"
# exec "$@"
