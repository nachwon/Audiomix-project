import os

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from pydub import AudioSegment

from config.settings import MEDIA_ROOT
from posts.models import Post



