FROM nachown/base
MAINTAINER  nachwon@naver.com

ENV         LANG C.UTF-8

WORKDIR     /srv/app
COPY        . /srv/app

# pyenv virtualenv
RUN         pyenv virtualenv 3.6.3 django_audio
RUN         pyenv local django_audio
RUN         /root/.pyenv/versions/django_audio/bin/pip install -r/srv/app/requirements.txt

# Nginx
RUN         cp /srv/app/.config/nginx/nginx.conf /etc/nginx/nginx.conf
RUN         cp /srv/app/.config/nginx/nginx.conf /etc/nginx/sites-available/
RUN         rm -rf /etc/nginx/sites-enabled/*
RUN         ln -sf /etc/nginx/sites-available/nginx.conf /etc/nginx/sites-enabled/nginx.conf

# uWSGI
RUN         mkdir -p /var/log/uwsgi/app

# manage.py
WORKDIR     /srv/app/Audiomix
RUN         /root/.pyenv/versions/django_audio/bin/python manage.py collectstatic --noinput
RUN         /root/.pyenv/versions/django_audio/bin/python manage.py migrate --noinput

# supervisor
RUN         cp /srv/app/.config/supervisor/* /etc/supervisor/conf.d/
CMD         supervisord -n

# port
EXPOSE      80