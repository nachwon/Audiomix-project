from PIL import Image

imagePath = '/home/che1/Projects/Django/django_audiomix/static/img/test.png'
newImagePath = '/home/che1/Projects/Django/django_audiomix/static/img/test2.png'
im = Image.open(imagePath)


# 이미지의 색을 바꿔주는 함수
def change_color(im):
    newimdata = []
    black1 = (51, 53, 51, 255)
    black2 = (50, 52, 50, 128)
    yellow1 = (226, 176, 38, 255)
    yellow2 = (225, 175, 37, 128)
    blank = (0, 0, 0, 0)
    for color in im.getdata():
        print(color)
        if color == black1:
            newimdata.append(yellow1)
        elif color == black2:
            newimdata.append(yellow2)
        else:
            newimdata.append(blank)
    newim = Image.new(im.mode, im.size)
    newim.putdata(newimdata)
    return newim


change_color(im).save(newImagePath)
