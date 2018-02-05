import re


def extension(filename):
    p = re.compile(r'.*[.](.*)')
    ext = p.match(filename).group(1)
    return ext


def author_track_directory_path(instance, filename):
    ext = extension(filename)
    return f'user_{instance.author.id}/Post_{instance.id}/author_track/author_track.{ext}'


def author_track_waveform_base_directory_path(instance, filename):
    return f'user_{instance.author.id}/Post_{instance.id}/author_track/author_track.png'


def author_track_waveform_cover_directory_path(instance, filename):
    return f'user_{instance.author.id}/Post_{instance.id}/author_track/author_track_cover.png'


def master_track_directory_path(instance, filename):
    ext = extension(filename)
    return f'user_{instance.author.id}/Post_{instance.id}/master_track/master_track.{ext}'


def master_track_waveform_base_directory_path(instance, filename):
    ext = extension(filename)
    return f'user_{instance.author.id}/Post_{instance.id}/master_track/waveform_base.{ext}'


def master_track_waveform_cover_directory_path(instance, filename):
    ext = extension(filename)
    return f'user_{instance.author.id}/Post_{instance.id}/master_track/waveform_cover.{ext}'


def comment_track_directory_path(instance, filename):
    ext = extension(filename)
    return f'user_{instance.post.author.id}/Post_{instance.post.id}/comment_tracks/comment_track_{instance.pk}.{ext}'


def post_img_directory_path(instance, filename):
    return f'user_{instance.author.id}/Post_{instance.id}/post_img/{filename}'
