#!/usr/bin/env bash
set -o nounset

python djlodging/django_app/manage.py collectstatic
python djlodging/django_app/manage.py migrate
nginx

exec "$@"
