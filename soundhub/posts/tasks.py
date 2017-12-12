from config import celery_app
from posts.models import Post
from utils.save_master_track import save_master_track


@celery_app.task(bind=True)
def mix_task(self, pk):
    post = Post.objects.get(pk=pk)
    save_master_track(post)

