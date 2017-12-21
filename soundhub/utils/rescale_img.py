import os
import random
import re

from PIL import Image

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage as storage

"""
프로필 이미지
200*200, 400*400

프로필 배경 이미지
750 x 422, 

앨범커버
750 x 750
"""


def rescale(img, size):
    src_width, src_height = img.size
    src_ratio = float(src_width) / float(src_height)
    dst_width, dst_height = size
    dst_ratio = float(dst_width) / float(dst_height)

    if dst_ratio < src_ratio:
        crop_height = src_height
        crop_width = crop_height * dst_ratio
        x_offset = int(src_width - crop_width) // 2
        y_offset = 0
    else:
        crop_width = src_width
        crop_height = crop_width / dst_ratio
        x_offset = 0
        y_offset = int(src_height - crop_height) // 3
    img_copy = img.copy()
    cropped = img_copy.crop((x_offset,
                             y_offset,
                             x_offset + int(crop_width),
                             y_offset + int(crop_height)))
    resized = cropped.resize((dst_width, dst_height), Image.ANTIALIAS)
    return resized


# 프로필 이미지 파일 생성
def make_profile_img(user, profile_img):
    sizes = ((200, 200), (400, 400))
    try:
        img = Image.open(profile_img)
    except ValueError:
        return None

    # profile_img 생성을 위한 로컬 경로
    directory = os.path.join(settings.MEDIA_ROOT, f'user_{user.pk}/profile_img')
    # 경로가 없으면 만들어줌
    if not os.path.exists(directory):
        os.makedirs(directory)

    img_list = list()
    for size in sizes:
        resized = rescale(img, size)
        filename = f'profile_img_{size[0]}.png'
        profile_dir = os.path.join(directory, filename)
        resized.save(profile_dir)
        img_list.append(profile_dir)

    save_img = img_list.pop()
    with open(save_img, 'rb') as f:
        file = ContentFile(f.read())

    user.profile_img.save(
        f'profile_img_{sizes[-1][0]}.png',
        file
    )
    os.remove(save_img)
    upload_to_s3(img_list)


# 프로필 배경이미지 생성
def make_profile_bg(user, profile_bg):
    size = (750, 422)
    try:
        img = Image.open(profile_bg)
    except ValueError:
        return None

    # profile_bg 생성을 위한 로컬 경로
    directory = os.path.join(settings.MEDIA_ROOT, f'user_{user.pk}/profile_bg')
    # 경로가 없으면 만들어줌
    if not os.path.exists(directory):
        os.makedirs(directory)
    img_list = list()

    resized = rescale(img, size)
    filename = f'profile_bg.png'
    profile_dir = os.path.join(directory, filename)
    resized.save(profile_dir)
    img_list.append(profile_dir)

    with open(profile_dir, 'rb') as f:
        file = ContentFile(f.read())

    user.profile_bg.save(
        'profile_bg.png',
        file,
    )
    os.remove(profile_dir)


# 포스트 배경이미지 생성
def make_post_img(post_img):
    size = (750, 750)
    try:
        img = Image.open(post_img)
    except ValueError:
        return None

    # profile_bg 생성을 위한 로컬 경로
    rand_int = random.randint(1, 100000)
    directory = os.path.join(settings.MEDIA_ROOT, f'post/{rand_int}/post_bg')
    # 경로가 없으면 만들어줌
    if not os.path.exists(directory):
        os.makedirs(directory)

    resized = rescale(img, size)

    filename = f'post_img.png'
    post_dir = os.path.join(directory, filename)
    resized.save(post_dir)

    with open(post_dir, 'rb') as f:
        file = ContentFile(f.read(), name=filename)

    return file, post_dir


def upload_to_s3(img_list):
    p = re.compile(r'.*/temp/(.*)')
    for img in img_list:
        s3_dir = p.match(img).group(1)
        file = storage.open(s3_dir, 'wb')
        with open(img, 'rb') as local_file:
            file.write(local_file.read())
        file.close()
        os.remove(img)
