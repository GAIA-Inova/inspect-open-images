import itertools
import sys
from models import *
from decouple import config
from PIL import Image, ImageDraw, ImageOps


def download_image(id=None):
    if id:
        train_image = TrainAnnotationImage.get(TrainAnnotationImage.imageid == id)
    else:
        train_image = TrainAnnotationImage.random_image()

    print(train_image.originalurl, train_image.rotation)
    train_image.download()
    return train_image


if __name__ == '__main__':
    train_image = download_image('68690e414ec7cbf1')
    image = train_image.image

    mask = Image.new("L", image.size, 0)
    for bbox in train_image.bboxes:
        w, h = train_image.image.width, train_image.image.height
        c1, c2 = bbox.coords
        c1 = (int(c1[0] * w), int(c1[1] * h))
        c2 = (int(c2[0] * w), int(c2[1] * h))


        draw = ImageDraw.Draw(mask)
        draw.rectangle([c1, c2], fill=255)
        #draw.rectangle([c1, c2], outline=0, width=2)
        #train_image.image.crop((itertools.chain(c1, c2)))
        ImageOps.crop(train_image.image, 40)

    image.putalpha(ImageOps.invert(mask))
    image.show()
