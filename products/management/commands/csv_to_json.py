# coding: utf8
import csv
import glob
import unicodedata
import re
import datetime
import json

from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand, CommandError

from products.models import Product, Maker, Genre


class Command(BaseCommand):
    def handle(self, *args, **options):
        today = datetime.datetime.now()
        for file in glob.glob('products/products/mobile/*.csv'):
            with open(file, 'r') as f:
                print(file)
                rows = csv.reader(f)
                next(rows)
                product_list = []
                for row in rows:
                    modelnumber = self.get_modelnumber(row[0])
                    genre       = self.get_genre(row[1])
                    maker       = self.get_maker(row[2])
                    thumbnail   = self.get_thumbnail(row[3])
                    image       = self.get_image(row[4], thumbnail)
                    manual      = self.get_manual(row[5])
                    productname = self.get_productname(row[6])
                    releasedate = self.get_releasedate(row[7])

                    if modelnumber == '':
                        break

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
                    product_list.append(info)

            with open("products/products/mobile.json", 'w') as f:
                json.dump(product_list, f, indent=2)


    def get_modelnumber(self, key):
        return unicodedata.normalize('NFKC', key.decode('utf8')).strip()

    def get_genre(self, key):
        return key
        # genre = Genre.objects.filter(name=key).first()
        # return genre

    def get_maker(self, key):
        with open('ethan_hunt/config/makers.json', 'r') as f:
            makers = json.load(f)
            if key:
                maker = re.sub('\(.+\)', '', key).strip().lower()
                if maker in makers:
                    maker = makers[maker]['makername']
                    return maker
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
        return key


