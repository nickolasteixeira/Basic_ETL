#!/bin/bash

# updates system
sudo apt-get update
# install pip
sudo apt-get install -y python-pip
sudo pip install -r requirements.txt

#installs postgres database
sudo apt-get install -y postgresql libpq-dev postgresql-client postgresql-client-common

# create a new user -> user of your linux operating system with your password
sudo -u postgres bash -c "psql -c \"CREATE USER $USER WITH PASSWORD 'yourpasswordhere';\""
sudo -u postgres bash -c "GRANT permissions ON DATABASE postgres TO $USER"
