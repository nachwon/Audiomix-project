from .base import *
import raven

# 데이터베이스 설정
DATABASES = config_secret['databases']['postgresql']

DEBUG = False

