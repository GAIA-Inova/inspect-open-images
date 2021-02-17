import io
import zipfile
from peewee import *
from decouple import config
from pathlib import Path
from PIL import Image
from cached_property import cached_property

import requests

database = SqliteDatabase(config('SQLITE_DB', default='./data/db.sqlite3'))

IMG_DOWNLOAD_DIR = Path(config('IMAGES_DOWNLOAD_DIR', default='./data/images'))
IMG_DOWNLOAD_DIR.mkdir(exist_ok=True, parents=True)
TRAIN_DATA_DIR = Path('./data')


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
    def label(self):
        return BoxAnnotationLabel.get(BoxAnnotationLabel.id == self.labelname).name

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

    @cached_property
    def image(self):
        return Image.open(self.image_path)

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

    @classmethod
    def by_id(cls, img_id):
        return cls.get(cls.imageid == img_id)

    def __str__(self):
        return str(self.images_dir)


class TrainAnnotationsObjectSegmentation(BaseModel):
    boxid = TextField(null=True)
    boxxmax = FloatField(null=True)
    boxxmin = FloatField(null=True)
    boxymax = FloatField(null=True)
    boxymin = FloatField(null=True)
    clicks = TextField(null=True)
    imageid = TextField(null=True)
    labelname = TextField(null=True)
    maskpath = TextField(null=True)
    predictediou = FloatField(null=True)

    class Meta:
        table_name = 'train_annotations_object_segmentation'
        primary_key = False

    @cached_property
    def train_image(self):
        return TrainAnnotationImage.by_id(self.imageid)

    @property
    def index(self):
        return self.imageid[0]

    @property
    def mask_image(self):
        zipname = TRAIN_DATA_DIR / f'train-masks-{self.index}.zip'
        imgs_zip = zipfile.ZipFile(zipname, 'r')
        img_data = imgs_zip.read(self.maskpath)
        return Image.open(io.BytesIO(img_data))

    @classmethod
    def random(cls):
        return cls.select().order_by(fn.Random()).limit(1).get()
