from django.apps import AppConfig
from django.db.models.signals import pre_save, post_save

from posts.signals import skip_saving_file, save_file


class PostsConfig(AppConfig):
    name = 'posts'

    def ready(self):
        Post = self.get_model('Post')
        pre_save.connect(skip_saving_file, sender=Post)
        post_save.connect(save_file, sender=Post)
