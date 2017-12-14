from PIL import Image

"""
프로필 이미지
200 x 200

프로필 배경 이미지
750 x 422, 

앨범커버
750 x 750
"""


def rescale(user, width, height, force=False):
    profile_img = user.profile_img

    img = Image.open(profile_img)

    if not force:
        img.thumbnail((width, height), Image.ANTIALIAS)

    filename = 'hello.png'
    img.save(filename)
    return data
