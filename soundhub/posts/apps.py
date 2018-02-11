from django.apps import AppConfig
from django.db.models.signals import pre_save, post_save, post_delete

from posts.signals import create_post, create_comment
from posts.signals.create_postlike import update_like


class PostsConfig(AppConfig):
    name = 'posts'

    def ready(self):
        Post = self.get_model('Post')
        pre_save.connect(create_post.skip_saving_file, sender=Post)
        post_save.connect(create_post.save_file, sender=Post)

        PostLike = self.get_model('PostLike')
        post_save.connect(update_like, sender=PostLike)
        post_delete.connect(update_like, sender=PostLike)

        CommentTrack = self.get_model('CommentTrack')
        pre_save.connect(create_comment.skip_saving_file, sender=CommentTrack)
        post_save.connect(create_comment.save_file, sender=CommentTrack)
