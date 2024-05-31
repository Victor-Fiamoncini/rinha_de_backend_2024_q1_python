FROM python:3.11.6-slim

# Installs python sys dependencies as admin user
RUN apt-get update \
    && apt-get install --no-install-recommends -y gcc g++ libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Creates and uses a "python" user
RUN useradd -ms /bin/bash python

# Switches to the new user and set the home directory as the working directory
WORKDIR /home/python
COPY --chown=python:python . .

# Switches to the new user for installing python packages
USER python

# Installs dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Checks that uwsgi is installed and available in the PATH
RUN /home/python/.local/bin/uwsgi --version

# Sets PATH environment variable
ENV PATH="/home/python/.local/bin:$PATH"

# Runs the WSGI server as the "python" user
CMD ["sh", "run_prod_server.sh"]
