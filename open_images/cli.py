import tqdm
import itertools
import sys
import threading, queue
from models import *
from decouple import config
from PIL import Image, ImageDraw, ImageOps
from concurrent.futures import ThreadPoolExecutor

IMAGES_QUEUE = queue.Queue()

def download_image(id=None):
    if id:
        train_image = TrainAnnotationImage.get(TrainAnnotationImage.imageid == id)
    else:
        train_image = TrainAnnotationImage.random_image()

    try:
        print(f'Downloading {train_image}')
        train_image.download()
        IMAGES_QUEUE.put(train_image)
        return train_image
    except:
        return None

def gen_images_from_crop(train_image):
    image = Image.open(train_image.image_path)

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

def gen_crops():
    while True:
        train_image = IMAGES_QUEUE.get()  # uma imagem foi infileirada para processamento
        if train_image is None:
            break

        print(f'Working on {train_image}')
        gen_images_from_crop(train_image)
        print(f'Finished {train_image}')

        IMAGES_QUEUE.task_done()

if __name__ == '__main__':
    threads = []
    for i in range(32):
        t = threading.Thread(target=gen_crops)
        t.start()
        threads.append(t)

    with ThreadPoolExecutor(max_workers=4) as executor:
        ids = [d.name for d in IMG_DOWNLOAD_DIR.iterdir()]
        for id in ids:
            executor.submit(download_image, id)

    print('joining queue...')
    IMAGES_QUEUE.join()

    for i in threads:
        IMAGES_QUEUE.put(None)
    for t in tqdm.tqdm(threads, desc='finishing threads'):
        t.join()
