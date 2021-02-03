import tqdm
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

    train_image.download()
    return train_image

def gen_images_from_crop(image_path):
    image = Image.open(image_path)

    mask = Image.new("L", image.size, 0)
    for bbox in train_image.bboxes:
        w, h = train_image.image.width, train_image.image.height
        c1, c2 = bbox.coords
        c1 = (int(c1[0] * w), int(c1[1] * h))
        c2 = (int(c2[0] * w), int(c2[1] * h))

        draw = ImageDraw.Draw(mask)
        draw.rectangle([c1, c2], fill=255)

    image.putalpha(ImageOps.invert(mask))
    image.save(str(train_image.border_image_path), 'PNG')

    image.putalpha(mask)
    image.save(str(train_image.content_image_path), 'PNG')


if __name__ == '__main__':
    for i in tqdm.tqdm(range(1000)):
        train_image = download_image()
        gen_images_from_crop(train_image.image_path)
