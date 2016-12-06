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
        for file in glob.glob('products/jusetsu/*.csv'):
            with open(file, 'r') as f:
                print(file)
                rows = csv.reader(f)
                next(rows)
                for row in rows:
                    unformatted_modelnumber = row[0]
                    unformatted_genre = row[1]
                    unformatted_maker = row[2]
                    unformatted_thumbnail = row[3]
                    unformatted_manual = row[4]
                    unformatted_productname = row[5]
                    unformatted_releasedate = row[6]

                    if not unformatted_modelnumber:
                        break

                    modelnumber = unicodedata.normalize('NFKC', unformatted_modelnumber.decode('utf8')).strip()

                    genre = self.get_genre_name(unformatted_genre)

                    maker = unicodedata.normalize('NFKC', unformatted_maker.decode('utf8')).strip()

                    if not unformatted_thumbnail or not 'http' in unformatted_thumbnail:
                        thumbnail = ''
                        images = []
                    else:
                        thumbnail = unformatted_thumbnail
                        images = [thumbnail]

                    if not unformatted_manual or not 'http' in unformatted_manual:
                        manual = ''
                    else:
                        manual = unformatted_manual

                    productname = unicodedata.normalize('NFKC', unformatted_productname.decode('utf8')).strip()

                    if unformatted_releasedate:
                        unformatted_releasedate = re.split('年|月|日', unformatted_releasedate)
                        if len(unformatted_releasedate) == 4:
                            if len(unformatted_releasedate[1]) == 1:
                                unformatted_releasedate[1] = '0' + unformatted_releasedate[1]
                            if len(unformatted_releasedate[2]) == 1:
                                unformatted_releasedate[2] = '0' + unformatted_releasedate[2]
                            unformatted_releasedate = "%s-%s-%s" % (unformatted_releasedate[0], unformatted_releasedate[1], unformatted_releasedate[2])
                            releasedate = datetime.datetime.strptime(unformatted_releasedate, '%Y-%m-%d')
                        if len(unformatted_releasedate) == 3:
                            if len(unformatted_releasedate[1]) == 1:
                                unformatted_releasedate[1] = '0' + unformatted_releasedate[1]
                            unformatted_releasedate = "%s-%s-01" % (unformatted_releasedate[0], unformatted_releasedate[1])
                            releasedate = datetime.datetime.strptime(unformatted_releasedate, '%Y-%m-%d')
                        if len(unformatted_releasedate) == 2:
                            releasedate = None
                    else:
                        releasedate = None


                    is_product = Product.objects.filter(modelnumber=modelnumber).first()
                    if is_product:
                        if not is_product.manual and manual:
                            is_product.manual = manual
                            is_product.save()
                        continue

                    with open('ethan_hunt/config/makers.json', 'r') as f:
                        makers = json.load(f)
                        if maker:
                            maker = re.sub('\(.+\)', '', maker).strip().lower()
                            if maker in makers:
                                maker = makers[maker]['makername']
                            else:
                                pass

                    maker = Maker.objects.filter(name=maker).first()
                    if maker is None:
                        print('maker name "%s" is not in database' % unformatted_maker)
                        continue

                    genre_name_list = genre.split('/')
                    genre = Genre.objects.filter(name=genre_name_list[-1]).first()

                    info = {
                        'modelnumber': modelnumber,
                        'productname': productname,
                        'maker': maker,
                        'jancode': '',
                        'genre': genre,
                        'releasedate': releasedate,
                        'thumbnail': thumbnail,
                        'image': images,
                        'manual': manual
                    }
                    print(info)
                    product = Product(**info)
                    product.save()

    def get_genre_name(self, key):
        genre_dict = {
            'ガス給湯器': '住宅設備/ガス給湯器',
            'ビルトインコンロ': '住宅設備/ビルトインコンロ',
            'IHクッキングヒーター': '住宅設備/IHクッキングヒーター',
            '温水洗浄便座': '住宅設備/温水洗浄便座',
            'エアコン': '空調・季節/エアコン',
            '換気扇': '住宅設備/換気扇',
            '電気温水器': '住宅設備/電気温水器',
            '石油給湯器': '住宅設備/石油給湯器',
            '火災警報器': '住宅設備/火災警報器',
            'ドアホン': '住宅設備/ドアホン',
            'ビルトインオーブンレンジ': '住宅設備/ビルトインオーブンレンジ',
            '食器洗い乾燥機': '住宅設備/食器洗い乾燥機',
            '洗面化粧台': '住宅設備/洗面化粧台',
            '照明機器': '照明/照明機器（直付・埋込）',
            'システムバス': '住宅設備/システムバス',
            'システムキッチン': '住宅設備/システムキッチン',
            'その他': '住宅設備/その他住宅設備'
        }
        return genre_dict[key]