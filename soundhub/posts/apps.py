from django.apps import AppConfig
from django.db.models.signals import pre_save, post_save, post_delete

from posts.signals.create_post import skip_saving_file, save_file
from posts.signals.create_postlike import update_like, update_unlike


class PostsConfig(AppConfig):
    name = 'posts'

    def ready(self):
        Post = self.get_model('Post')
        pre_save.connect(skip_saving_file, sender=Post)
        post_save.connect(save_file, sender=Post)

        PostLike = self.get_model('PostLike')
        post_save.connect(update_like, sender=PostLike)
        post_delete.connect(update_unlike, sender=PostLike)
