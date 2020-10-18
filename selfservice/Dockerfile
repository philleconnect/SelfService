FROM debian:buster-slim

MAINTAINER Johannes Kreutz <sc@jkm-marburg.de>

ENV DEBIAN_FRONTEND noninteractive

ENV VERSION "1"

USER root

RUN apt-get update && apt-get install -y --no-install-recommends nginx openssl openssh-client sudo mariadb-client ca-certificates python3 python3-flask python3-requests python3-passlib python3-bcrypt python3-pip python3-setuptools python3-flask-login uwsgi uwsgi-plugin-python3 wkhtmltopdf python3-pdfkit
RUN pip3 install Flask-Session mysql-connector
RUN apt-get purge -y python3-pip python3-setuptools
RUN apt-get autoremove -y

RUN mkdir /usr/local/bin/selfservice
ADD selfservice /usr/local/bin/selfservice

ADD ui /var/www/html
RUN chown -R www-data /var/www/html/

COPY default /etc/nginx/sites-enabled/

RUN mkdir /etc/selfservice

EXPOSE 80

COPY entrypoint.sh /
RUN chmod +x /entrypoint.sh

CMD ["./entrypoint.sh"]
