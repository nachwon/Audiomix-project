def update_like(sender, instance, created=False, **kwargs):
    instance.post.num_liked = instance.post.liked.count()

    instance.post.save()
