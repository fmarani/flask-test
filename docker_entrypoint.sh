#!/bin/sh

python manage.py recreate_db
python manage.py dev_server
