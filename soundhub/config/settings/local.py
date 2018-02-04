from .base import *

# 데이터베이스 설정
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

MEDIA_URL = '/temp/'
STATIC_URL = '/static/'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
