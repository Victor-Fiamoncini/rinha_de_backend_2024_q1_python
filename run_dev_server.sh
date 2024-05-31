#!/bin/sh

python -m flask cli create-database

python -m flask db upgrade

python -m flask cli create-clients

python -m flask run --debug --host=0.0.0.0
