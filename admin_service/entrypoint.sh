#!/usr/bin/env bash

set -e

python manage.py compilemessages -l en -l ru
python manage.py migrate --fake movies 0001_initial
python manage.py migrate
python manage.py collectstatic --no-input
cd sqlite_to_postgres && python load_data.py

uwsgi --strict --ini /opt/app/uwsgi.ini