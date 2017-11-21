FROM nachown/base
MAINTAINER  nachwon@naver.com

ENV         LANG C.UTF-8

WORKDIR     /srv/app
COPY        . /srv/app

# pyenv virtualenv
RUN         pyenv local app
RUN         /root/.pyenv/versions/app/bin/pip install -r /srv/app/requirements.txt

# Nginx
RUN         cp /srv/app/.config/nginx/nginx.conf /etc/nginx/
RUN         cp /srv/app/.config/nginx/soundhub.conf /etc/nginx/sites-available/
RUN         rm -rf /etc/nginx/sites-enabled/*
RUN         ln -sf /etc/nginx/sites-available/soundhub.conf /etc/nginx/sites-enabled/

# uWSGI
RUN         mkdir -p /var/log/uwsgi/app

# manage.py
WORKDIR     /srv/app/soundhub
RUN         /root/.pyenv/versions/app/bin/python /srv/app/soundhub/manage.py collectstatic --noinput
RUN         /root/.pyenv/versions/app/bin/python /srv/app/soundhub/manage.py migrate --noinput

# supervisor
RUN         cp /srv/app/.config/supervisor/* /etc/supervisor/conf.d/
CMD         supervisord -n

# port
EXPOSE      80