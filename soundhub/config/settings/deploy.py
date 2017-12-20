from .base import *
import raven

# 데이터베이스 설정
DATABASES = config_secret['databases']['postgresql']

DEBUG = False

RAVEN_CONFIG = {
    'dsn': 'https://e01ad1cebe374afba306dd30c0c95aec:f188b0f719e24508946c5ab72b4de3c8@sentry.io/259770',
    # If you are using git, you can also automatically configure the
    # release based on the git info.
    'release': raven.fetch_git_sha(os.path.abspath(os.pardir)),
}