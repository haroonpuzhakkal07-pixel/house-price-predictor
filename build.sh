#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python django_app/manage.py collectstatic --noinput