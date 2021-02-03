from peewee import *
from decouple import config
from pathlib import Path
from PIL import Image

import requests

database = SqliteDatabase(config('SQLITE_DB', default='./data/db.sqlite3'))

IMG_DOWNLOAD_DIR = Path(config('IMAGES_DOWNLOAD_DIR', default='./data/images'))
IMG_DOWNLOAD_DIR.mkdir(exist_ok=True, parents=True)


class UnknownField(object):
    def __init__(self, *_, **__): pass

class BaseModel(Model):
    class Meta:
        database = database

class BoxAnnotationLabel(BaseModel):
    id = TextField(null=True)
    name = TextField(null=True)

    class Meta:
        table_name = 'oidv6_class_descriptions_boxable'
        primary_key = False

class TrainAnnotationBoundingBox(BaseModel):
    confidence = IntegerField(null=True)
    imageid = TextField(null=True)
    isdepiction = IntegerField(null=True)
    isgroupof = IntegerField(null=True)
    isinside = IntegerField(null=True)
    isoccluded = IntegerField(null=True)
    istruncated = IntegerField(null=True)
    labelname = TextField(null=True)
    source = TextField(null=True)
    xclick1x = FloatField(null=True)
    xclick1y = FloatField(null=True)
    xclick2x = FloatField(null=True)
    xclick2y = FloatField(null=True)
    xclick3x = FloatField(null=True)
    xclick3y = FloatField(null=True)
    xclick4x = FloatField(null=True)
    xclick4y = FloatField(null=True)
    xmax = FloatField(null=True)
    xmin = FloatField(null=True)
    ymax = FloatField(null=True)
    ymin = FloatField(null=True)

    class Meta:
        table_name = 'oidv6_train_annotations_bbox'
        primary_key = False

    @property
    def coords(self):
        return (
            (self.xmin, self.ymin),
            (self.xmax, self.ymax),
        )

    @classmethod
    def get_image_bboxes(cls, image_id):
        return cls.select().where(cls.imageid == image_id)

class TrainAnnotationImage(BaseModel):
    author = TextField(null=True)
    authorprofileurl = TextField(null=True)
    imageid = TextField(null=True)
    license = TextField(null=True)
    originallandingurl = TextField(null=True)
    originalmd5 = TextField(null=True)
    originalsize = IntegerField(null=True)
    originalurl = TextField(null=True)
    rotation = FloatField(null=True)
    subset = TextField(null=True)
    thumbnail300kurl = TextField(null=True)
    title = TextField(null=True)

    class Meta:
        table_name = 'train_images_boxable_with_rotation'
        primary_key = False

    @property
    def image_suffix(self):
        return Path(self.originalurl).suffix

    @property
    def images_dir(self):
        return IMG_DOWNLOAD_DIR / f'{self.imageid}'

    @property
    def image_path(self):
        return self.images_dir / f'original{self.image_suffix}'

    @property
    def border_image_path(self):
        return self.images_dir / 'border.png'

    @property
    def content_image_path(self):
        return self.images_dir / 'content.png'

    @property
    def bboxes(self):
        return TrainAnnotationBoundingBox.get_image_bboxes(self.imageid)

    def download(self):
        if not self.image_path.exists():
            response = requests.get(self.originalurl)
            if not response.ok:
                raise Exception(f'Invalid response: {response.status_code}')

            self.images_dir.mkdir(exist_ok=True, parents=True)
            with open(self.image_path, 'wb') as fd:
                fd.write(response.content)

    @classmethod
    def random_image(cls):
        return cls.select().order_by(fn.Random()).limit(1).get()

    def __str__(self):
        return str(self.images_dir)
