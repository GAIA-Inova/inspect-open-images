from models import *
from decouple import config


def download_image(id=None):
    if id:
        train_image = TrainAnnotationImage.get(imageid == id)
    else:
        train_image = TrainAnnotationImage.random_image()

    print(train_image.originalurl, train_image.rotation)
    train_image.download()


if __name__ == '__main__':
    download_image()
