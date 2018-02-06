def update_like(sender, instance, created, **kwargs):
    instance.post.num_liked = instance.post.liked.count()

    instance.post.save()


def update_unlike(sender, instance, **kwargs):
    instance.post.num_liked = instance.post.liked.count()

    instance.post.save()
