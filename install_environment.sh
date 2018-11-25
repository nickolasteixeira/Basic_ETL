#!/bin/bash

# updates system
sudo apt-get update
# install pip
sudo apt-get install -y python3-pip
sudo pip3 install -r requirements.txt

#installs postgres database
sudo apt-get install -y postgresql libpq-dev postgresql-client postgresql-client-common

# create a new user -> user of your linux operating system with your password
sudo -u postgres bash -c "psql -c \"CREATE USER $USER WITH PASSWORD 'yourpasswordhere';\""
sudo -u postgres bash -c "psql -c \"GRANT ALL PRIVILEGES ON DATABASE postgres TO $USER;\""
sudo -u postgres bash -c "psql -c \"ALTER ROLE $USER WITH SUPERUSER\""
