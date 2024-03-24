#!/bin/bash

python -m flask db upgrade

python -m flask --app rinha_de_backend_2024_q1/app run --debug --host=0.0.0.0
