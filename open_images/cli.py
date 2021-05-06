#!/usr/bin/env python3

import click
import tqdm
import itertools
import sys
import threading, queue
from requests.exceptions import HTTPError
from models import *
from decouple import config
from PIL import Image, ImageDraw, ImageOps
from concurrent.futures import ThreadPoolExecutor



@click.group()
def command_line_entrypoint():
    """
    Ferramenta pra explorar imagens do dataset Open Images V6
    """
    pass


def download_image(img_id=None):
    if img_id:
        train_image = TrainAnnotationImage.by_id(img_id)
    else:
        train_image = TrainAnnotationImage.random_image()

    print(f'Baixando {train_image}')
    train_image.download()
    return train_image

def gen_images_from_crop(train_image):
    image = train_image.image

    mask = Image.new("L", image.size, 0)

    for i, bbox in enumerate(train_image.bboxes, start=1):
        label = bbox.label
        w, h = image.width, image.height
        c1, c2 = bbox.coords
        c1 = (int(c1[0] * w), int(c1[1] * h))
        c2 = (int(c2[0] * w), int(c2[1] * h))

        area = (c1[0], c1[1], c2[0], c2[1])
        crop = image.crop(area)
        crop.save(str(train_image.images_dir / f"{i:0>2d}-{label}.png"), 'PNG')

        draw = ImageDraw.Draw(mask)
        draw.rectangle([c1, c2], fill=255)

    image.putalpha(ImageOps.invert(mask))
    image.save(str(train_image.border_image_path), 'PNG')

    image.putalpha(mask)
    image.save(str(train_image.content_image_path), 'PNG')


@command_line_entrypoint.command('bbox')
@click.option('--img-id', '-i')
@click.option('--quantity', '-q', default=5)
def bbox(quantity, img_id):
    """
    Baixa imagens de treinamento do dataset e, para cada uma nova delas,
    gera novas images divididas por 3 tipos de categoria:

    - Conteúdo: uma única imagem composta apenas pelos conteúdos dos
    bouding boxes com as anotações sobre a imagem. O arquivo final chama-se
    `content.png`.
    - Borda: uma única imagem composta pelas áreas da imagem não compreendidas
    pelo conjunto de áreas delimitadas pelos bounding boxes com anotações da
    imagem. O arquivo final chama-se `border.png`.
    - Objetos: várias imagens, uma para cada objeto anotado na imagem original,
    sendo um recorte do objeto em si. Por exemplo, se uma das imagens possui uma
    anotação de uma pessoa em uma área de 64x220 pixels, isso resultará em um
    arquivo nomeado `01-person.png` coa mesma dimensão da área da anotação.
    """
    threads = []
    if img_id:
        train_image = download_image(img_id=img_id)
        print(f'Gerando {train_image}')
        gen_images_from_crop(train_image)
        print(f'FINALIZADO {train_image}')
        return


    for i in range(quantity):
        try:
            train_image = download_image()
            print(f'Gerando {train_image}')
            gen_images_from_crop(train_image)
            print(f'FINALIZADO {train_image}')
        except HTTPError as e:
            print(f"Erro: {e}")


@command_line_entrypoint.command('segmentation')
@click.option('--img-id', '-i')
@click.option('--quantity', '-q', default=5)
def gen_segmentation_images(quantity, img_id):
    segmentations = TrainAnnotationsObjectSegmentation.from_random_image()
    for i, segmentation in enumerate(segmentations, start=1):
        label = segmentation.label

        mask = segmentation.mask_image
        train_image = download_image(segmentation.imageid)
        image = train_image.image

        if mask.size == image.size:
            image.putalpha(mask)
            image.save(str(train_image.images_dir / f'seg-{i}-{label}.png'), 'PNG')
        else:
            print('Tamanho de máscaras e imagem diferentes')
            break


if __name__ == "__main__":
    command_line_entrypoint()
