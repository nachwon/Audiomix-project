from django.db import models


class Post(models.Model):
    author = models.CharField(max_length=50)
    title = models.CharField(max_length=100)
    track = models.FileField(upload_to='tracks/')

    def __str__(self):
        return f'Post: {self.title}'


class Commit(models.Model):
    author = models.CharField(max_length=50)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    INST_CHOICES = (
        ('V', 'Vocal'),
        ('G', 'Guitar'),
        ('B', 'Bass'),
        ('D', 'Drums'),
        ('K', 'Keyboard'),
        ('O', 'Others'),
    )
    instrument = models.CharField(max_length=1, choices=INST_CHOICES)
    commit = models.FileField(upload_to='commits/')

    def __str__(self):
        return f'Post: {self.post.title} - {self.instrument}'
