import os
from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# 설정 모듈 불러옴
app = Celery('config')

# django.conf.setting 에서 CELERY 로 시작하는 모든 변수를 가져온다
app.config_from_object('django.conf:settings', namespace='CELERY')

# 장고 앱 안에 있는 모든 tasks.py 모듈을 불러온다
app.autodiscover_tasks()

