from .base import *
import raven

# 데이터베이스 설정
DATABASES = config_secret['databases']['postgresql']

# S3 저장소 설정
DEFAULT_FILE_STORAGE = 'config.storages.MediaStorage'
STATICFILES_STORAGE = 'config.storages.StaticStorage'
MEDIAFILES_LOCATION = 'media'
STATICFILES_LOCATION = 'static'

DEBUG = False

