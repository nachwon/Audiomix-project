import os
import re

from PIL import Image

from django.conf import settings
from django.core.files.storage import default_storage as storage

"""
프로필 이미지
200*200, 400*400

프로필 배경 이미지
750 x 422, 

앨범커버
750 x 750
"""


# 프로필 이미지 파일 생성
def make_profile_img(user):
    profile_img = user.profile_img
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
    if img.width == img.height:
        for size in sizes:
            img_copy = img.copy()
            img_copy.thumbnail(size, Image.ANTIALIAS)
            filename = f'profile_img_{size[0]}.png'
            profile_dir = os.path.join(directory, filename)
            img_copy.save(profile_dir)
            img_list.append(profile_dir)

    else:
        src_width, src_height = img.size
        src_ratio = float(src_width) / float(src_height)
        for size in sizes:
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
            filename = f'profile_img_{size[0]}.png'
            profile_dir = os.path.join(directory, filename)
            resized.save(profile_dir)
            img_list.append(profile_dir)
    return img_list


def upload_to_s3(img_list):
    p = re.compile(r'.*/temp/(.*)')

    for img in img_list:
        s3_dir = p.match(img).group(1)
        file = storage.open(s3_dir, 'wb')
        with open(img, 'rb') as local_file:
            file.write(local_file.read())
        file.close()
        os.remove(img)


def destroy_from_s3(user):
    path_200 = f'user_{user.pk}/profile_img/profile_img_200.png'
    path_400 = f'user_{user.pk}/profile_img/profile_img_400.png'
    if storage.exists(path_200) and storage.exists(path_400):
        storage.delete(path_200)
        storage.delete(path_400)
    else:
        return None
