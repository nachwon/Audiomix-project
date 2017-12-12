import os

SETTINGS_MODULE = os.environ.get('DJANGO_SETTINGS_MODULE')

if not SETTINGS_MODULE or SETTINGS_MODULE == 'config.settings.local':
    from .local import *

elif SETTINGS_MODULE == 'config.settings.deploy':
    from .deploy import *
