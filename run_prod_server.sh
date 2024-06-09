#!/bin/sh

python -m flask cli create-database

python -m flask db upgrade

python -m flask cli create-clients

uwsgi --ini wsgi.ini
