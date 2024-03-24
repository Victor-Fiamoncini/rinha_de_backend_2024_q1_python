FROM python:3.11.6-slim

# Installs python sys dependencies as admin user
RUN apt-get update \
    && apt-get install --no-install-recommends -y gcc g++ libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Creates and uses a "python" sys user
RUN useradd -ms /bin/bash python
USER python

# Installs virtualenv
RUN python -m pip install virtualenv

WORKDIR /home/python/app_dev
COPY . .

# Initializes virtualenv & installs dependencies
RUN python -m virtualenv venv
RUN pip install -r requirements.txt
RUN pip install -r requirements_dev.txt
