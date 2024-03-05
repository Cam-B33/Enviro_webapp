# Deploy Web front end to Var WWW, automated with a bash script

#!/bin/bash

# Path to the development directory
DEV_DIR="/home/cameron/Documents/gis-edna-app/www/"

# Path to the deployment directory
DEPLOY_DIR="/var/www/yourapp"

# Rsync to copy files, excluding .git
sudo rsync -av --progress $DEV_DIR $DEPLOY_DIR --exclude '.git'
