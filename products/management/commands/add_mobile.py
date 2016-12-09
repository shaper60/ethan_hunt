# coding: utf8
import csv
import glob
import unicodedata
import re
import datetime
import json

from django.core.management.base import BaseCommand, CommandError

from products.models import Product, Maker, Genre


class Command(BaseCommand):
    def handle(self, *args, **options):
        print('hello')
        for file in glob.glob('products/products/mobile/*.csv'):
            with open(file, 'r') as f:
                print(file)
                rows = csv.reader(f)
                next(rows)
                for row in rows:
                    modelnumber = self.get_modelnumber(row[0])
                    genre       = self.get_genre(row[1])
                    maker       = self.get_maker(row[2])
                    thumbnail   = self.get_thumbnail(row[3])
                    image       = self.get_image(row[4], thumbnail)
                    manual      = self.get_manual(row[5])
                    productname = self.get_productname(row[6])
                    releasedate = self.get_releasedate(row[7])

                    is_product = Product.objects.filter(modelnumber=modelnumber).first()
                    if is_product:
                        # if not is_product.manual and manual:
                        #     is_product.manual = manual
                        #     is_product.save()
                        continue

                    if maker is None:
                        print('maker name "%s" is not in database' % row[2])
                        continue

                    info = {
                        'modelnumber': modelnumber,
                        'genre': genre,
                        'maker': maker,
                        'thumbnail': thumbnail,
                        'manual': manual,
                        'productname': productname,
                        'releasedate': releasedate,
                        'image': image,
                        'jancode': ''
                    }
                    print(info)
                    # product = Product(**info)
                    # product.save()

    def get_modelnumber(self, key):
        return unicodedata.normalize('NFKC', key.decode('utf8')).strip()

    def get_genre(self, key):
        genre = Genre.objects.filter(name=key).first()
        return genre

    def get_maker(self, key):
        with open('ethan_hunt/config/makers.json', 'r') as f:
            makers = json.load(f)
            if key:
                maker = re.sub('\(.+\)', '', key).strip().lower()
                if maker in makers:
                    maker = makers[maker]['makername']
                    return Maker.objects.filter(name=maker).first()
                else:
                    return None

        return key

    def get_thumbnail(self, key):
        if not key or not 'http' in key:
            return ''
        else:
            return key

    def get_image(self, key, thumbnail):
        if key:
            image = [item.strip() for item in key.split(',')]
            return image
        elif thumbnail:
            return [thumbnail]
        else:
            return []

    def get_manual(self, key):
        if not key or not 'http' in key:
            return ''
        else:
            return key

    def get_productname(self, key):
        return unicodedata.normalize('NFKC', key.decode('utf8')).strip()

    def get_releasedate(self, key):
        if not key:
            return None
        releasedate = datetime.datetime.strptime(key, '%Y-%m-%d')
        return releasedate


