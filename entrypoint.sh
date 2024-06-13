#!/bin/bash
python proj/manage.py migrate
python proj/manage.py createcachetable
django-admin compilemessages
python proj/manage.py runserver 0.0.0.0:8000