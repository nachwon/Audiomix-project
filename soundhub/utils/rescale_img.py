from io import BytesIO
from PIL import Image


def rescale(data, width, height, force=False):
    data = BytesIO(data.read())
    img = Image.open(data)

    if not force:
        img.thumbnail((width, height), Image.ANTIALIAS)

    image_file = BytesIO()
    img.save(image_file, 'JPEG')
    data.file = image_file
    return data
