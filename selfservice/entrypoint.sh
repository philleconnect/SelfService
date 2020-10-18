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

# generate https key and certificate
if [ ! -f /etc/selfservice/privkey.pem ]; then
    openssl genrsa -out /etc/selfservice/privkey.pem 2048
    openssl req -new -x509 -key /etc/selfservice/privkey.pem -out /etc/selfservice/cacert.pem -days 36500 -subj "/C=DE/ST=Germany/L=Germany/O=SchoolConnect/OU=Schulserver/CN=example.com"
fi
cp /etc/selfservice/privkey.pem /etc/nginx/privkey.pem
cp /etc/selfservice/cacert.pem /etc/nginx/cacert.pem

echo "waiting for database..."
while ! mysqladmin ping -h"main_db" --silent; do
    sleep 1
done
echo 'everything is prepared, starting server for selfservice'
cd /usr/local/bin/selfservice
uwsgi --ini selfservice.ini --lazy &
cd
nginx -g 'daemon off;' &
NGINX_PROCESS=$!
wait $NGINX_PROCESS
