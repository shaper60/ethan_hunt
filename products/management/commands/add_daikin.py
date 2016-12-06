# coding: utf8
import csv
import datetime

from django.core.management.base import BaseCommand, CommandError

from products.models import Product, Maker, Genre


class Command(BaseCommand):
    def handle(self, *args, **options):
        with open('products/jusetsu/daikin/daikin_20161118.csv', 'r') as f:
            rows = csv.reader(f)
            next(rows)
            for row in rows:
                maker = Maker.objects.filter(name='DAIKIN').first()
                modelnumber = row[1]
                productname = "%s %s" % (row[2], modelnumber)
                jancode = row[14]
                releasedate = self.get_releasedate(row[15])
                genre = self.get_genre_name(row[17])
                manual = self.get_manual(row[28])
                thumbnail = self.get_thumbnail(row[27])
                image = self.get_image(thumbnail)


                is_product = Product.objects.filter(modelnumber=modelnumber).first()
                if is_product:
                    if not is_product.manual and manual:
                        is_product.manual = manual
                        is_product.save()
                    continue

                info = {
                    'maker': maker,
                    'modelnumber': modelnumber,
                    'productname': productname,
                    'jancode': jancode,
                    'releasedate': releasedate,
                    'genre': genre,
                    'manual': manual,
                    'thumbnail': thumbnail,
                    'image': image
                }
                print(info)
                product = Product(**info)
                product.save()

    def get_releasedate(self, key):
        releasedate = datetime.datetime.strptime(key, '%Y%m')
        return releasedate

    def get_genre_name(self, key):
        genre_dict = {
            'RA一般(小型)': '空調・季節/エアコン',
            'RA一般(中型)': '空調・季節/エアコン',
            'RA一般(大型)': '空調・季節/エアコン',
            'RA量販(小型)': '空調・季節/エアコン',
            'RA量販(中型)': '空調・季節/エアコン',
            'RA量販(大型)': '空調・季節/エアコン',
            '住宅用空気清浄器': '空調・季節/空気清浄機',
            'ｴｺｷｭｰﾄ': '住宅設備/電気温水器',
            'ﾈｵｷｭｰﾄ': '住宅設備/電気温水器',
            'ｽﾎﾟｯﾄ暖房機': '空調・季節/セラミックヒーター'
        }
        genre_name_list = genre_dict[key].split('/')
        genre = Genre.objects.filter(name=genre_name_list[-1]).first()
        return genre

    def get_manual(self, key):
        if key:
            return 'https://s3-ap-northeast-1.amazonaws.com/home-appliance/manuals/daikin/{}.pdf'.format(key)
        else:
            return ''

    def get_thumbnail(self, key):
        if key:
            return 'https://s3-ap-northeast-1.amazonaws.com/home-appliance/images/daikin/{}'.format(key)
        else:
            return ''

    def get_image(self, thumbnail):
        if thumbnail:
            return [thumbnail]
        else:
            return []