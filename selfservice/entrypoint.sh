#!/bin/bash

# Function for a clean shutdown of the container
function shutdown {
    kill -TERM "$NGINX_PROCESS" 2>/dev/null
    exit
}
trap shutdown SIGTERM

chmod 0777 /home
chmod 0777 /home/*

# Write the shared secret of the management apis to a permanent file
echo $MANAGEMENT_APIS_SHARED_SECRET > /etc/selfservice/managementsecret.txt

echo "waiting for database..."
while ! mysqladmin ping -h"main_db" --silent; do
    sleep 1
done
echo 'everything is prepared, starting server for selfservice'
python3 /usr/local/bin/selfservice/main.py &
nginx -g 'daemon off;' &
NGINX_PROCESS=$!
wait $NGINX_PROCESS
