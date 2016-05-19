# coding: utf-8
import datetime

from django.db import models
from django.contrib.auth.models import User

from model_utils.models import TimeStampedModel
from jsonfield import JSONField

from products.utils import pkgen


class Category(models.Model):
    """"車、家電などのGenreの上に立つモデル"""
    name = models.CharField(max_length=20)
    display_name = models.CharField(max_length=100)
    empty_title = models.CharField(max_length=200, default='')

def appliance():
    obj, created = Category.objects.get_or_create(name='appliance', display_name='家電')
    return obj.pk

class Genre(TimeStampedModel):
  """
  製品のジャンルのモデル
  """
  WHITE_GOODS = 'WG'
  BLACK_GOODS = 'BG'
  PC_DEVICES  = 'PD'
  MOBILE_DEVICES = 'MD'
  OTHERS = 'OT'

  GENERIC_NAMES = (
    (WHITE_GOODS, 'White Goods'),
    (BLACK_GOODS, 'Black Goods'),
    (PC_DEVICES, 'PC Devices'),
    (MOBILE_DEVICES, 'Mobile Devices'),
    (OTHERS, 'Others')
  )

  name = models.CharField(max_length=100)         # ジャンル名
  parent = models.ForeignKey('self', null=True, blank=True, default=None)   # 上の階層(Genre)
  category = models.ForeignKey(Category, default=appliance)
  generic_name = models.CharField(max_length=3, choices=GENERIC_NAMES, default=WHITE_GOODS)

  @property
  def children(self):
    return Genre.objects.filter(parent=self)

  def dumps(self):
    pass

  def __str__(self):
    return u'<Genre %s>' % self.name

  def __unicode__(self):
    return u'<Genre %s>' % self.name

class Maker(TimeStampedModel):
  """
  メーカー名のモデル
  """
  name = models.CharField(max_length=100)         # メーカー名

  def dumps(self):
    return {
      'name': self.name
    }

  def __str__(self):
    return u'<Maker %s>' % self.name

  def __unicode__(self):
    return u'<Maker %s>' % self.name

class Product(TimeStampedModel):
  """製品マスターのモデル"""
  object_id = models.CharField(max_length=16,
    primary_key=True, default=pkgen)              # ランダムID
  productname = models.TextField(max_length=100)  # 製品名 (String)
  jancode = models.CharField(max_length=48)       # ジャンコード (String)
  modelnumber = models.TextField(max_length=50)   # 型番 (String)
  detail = JSONField(default={})                  # 詳細 (ハッシュオブジェクト)
  genre = models.ForeignKey(Genre, null=True)     # ジャンル (Genreオブジェクト)
  thumbnail = models.URLField(max_length=1096)    # リストで表示させる小さい画像 (URL)
  image = JSONField(default=[])                   # 詳細ページで表示させる大きい画像 (URL)
  maker = models.ForeignKey(Maker, null=True)     # メーカー名
  price = JSONField(default={})                   # 製品の値段 (ハッシュオブジェクト)
  upper_limit_price = models.IntegerField(null=True, default=None, blank=True)
  lower_limit_price = models.IntegerField(null=True, default=None, blank=True)
  manual = models.URLField(max_length=1096)       # 製品マニュアルのリンクURL (URL)
  releasedate = models.DateField(null=True)       # 発売日 (Date)
  warranty_duration = models.DurationField(default=datetime.timedelta(days=365))

  def to_dict(self):
    h = {
      "name": self.productname,
      "kataban": self.modelnumber,
      "jancode": self.jancode,
    }
    if len(self.image) > 0:
        h['image'] = self.image[0]
    else:
        h['image'] = 'https://s3.amazonaws.com/apiv2/noimage.png'
    if self.maker is not None:
      h['maker'] = self.maker.name
    return h

  def dumps(self):
    """
    @return params: Productのメンバー
    @rtype params: dict
    """
    h = {
      'object_id': self.object_id,
      'name': self.productname,
      'jancode': self.jancode,
      'modelnumber': self.modelnumber,
      'detail': self.detail,
      'image': self.image,
      'thumbnail': self.thumbnail,
      'manual': self.manual,
      'genre': '',
      'maker': '',
      'releasedate': ''
    }
    if self.genre is not None:
      h['genre'] = self.genre.name
    if self.maker is not None:
      h['maker'] = self.maker.name
    return h

  def dict_for_trigger(self):
    h = {
      'object_id': self.object_id,
      'name': self.productname,
      'jancode': self.jancode,
      'modelnumber': self.modelnumber,
      'detail': self.detail,
      'image[]': self.image,
      'thumbnail': self.thumbnail,
      'manual': self.manual,
      'genre': '',
      'maker': '',
      'releasedate': ''
    }
    if self.genre is not None:
      h['genre'] = self.genre.name
    if self.maker is not None:
      h['maker'] = self.maker.name
    return h

  def __str__(self):
    return u'<Product model={}>'.format(self.modelnumber)

  def __unicode__(self):
    return u'<Product model={}>'.format(self.modelnumber)

  def admin_image(self):
    if len(self.image) > 0:
      return '<img src="{}" style="width:40px;height:auto;">'.format(self.image[0])
    else:
      return 'no image'

  def admin_thumbnail(self):
    if len(self.thumbnail) > 0:
      return '<img src="{}" style="width:40px;height:auto;">'.format(self.thumbnail)
    else:
      return 'no image'

  admin_image.allow_tags = True
  admin_thumbnail.allow_tags = True
