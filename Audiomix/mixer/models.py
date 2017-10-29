from django.db import models

class Audio(models.Model):
    track = models.FileField(upload_to='tracks/')
