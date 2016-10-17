# coding: utf-8
import json
import glob
import re
import datetime

from django.core.management.base import BaseCommand, CommandError

from products.models import Product, Maker, Genre


class Command(BaseCommand):
    def handle(self, *args, **options):
        for file in glob.glob('products/products/*.json'):
            with open(file, 'r') as f:
                print(f.name)
                products = json.load(f)
                for product in products:
                    print(product['modelnumber'])
                    is_product = Product.objects.filter(modelnumber=product['modelnumber']).first()
                    if is_product:
                        if not is_product.manual and product['manual']:
                            print('update manual')
                            is_product.manual = product['manual']
                            is_product.save()
                        continue


                    with open('ethan_hunt/config/makers.json', 'r') as f:
                        makers = json.load(f)
                        if product['maker']:
                            maker = re.sub('\(.+\)', '', product['maker']).strip().lower()
                            if maker in makers:
                                product['maker'] = makers[maker]['makername']
                            else:
                                pass

                    # 保存したいけど、postgresにメーカーデータがないため、保存を断念
                    maker = Maker.objects.filter(name=product['maker']).first()
                    if maker is None:
                        print('maker name "%s" is not in database' % product['maker'])
                        continue


                    with open('ethan_hunt/config/genres.json', 'r') as f:
                        genres = json.load(f)
                        genre_name = product['genre']
                        if genre_name in genres:
                            product['genre'] = genres[genre_name]
                        else:
                            pass

                    # 保存したいけど、postgresにジャンルデータがないため、保存を断念
                    genre_name_list = product['genre'].split('/')
                    genre = Genre.objects.filter(name=genre_name_list[-1]).first()
                    if genre is None:
                        print('genre name "%s" is not in database' % product['genre'])
                        continue


                    if product['jancode'] is None:
                        product['jancode'] = ''

                    if not 'manual' in product:
                        product['manual'] = ''
                    elif product['manual'] is None:
                        product['manual'] = ''

                    if product['thumbnail'] is None:
                        product['thumbnail'] = ''

                    releasedate = product['releasedate']
                    if releasedate and re.search('\[', releasedate):
                        releasedate = datetime.datetime.strptime(releasedate, '%Y-%m-%d')
                    elif releasedate:
                        releasedate = releasedate.rstrip('T')

                    info = {
                        'modelnumber': product['modelnumber'],
                        'productname': product['productname'],
                        'maker': maker,
                        'jancode': product['jancode'],
                        'genre': genre,
                        'releasedate': releasedate,
                        # 'detail': product['detail'],
                        'thumbnail': product['thumbnail'],
                        'image': product['images'],
                        'manual': product['manual']
                    }
                    print(info)
                    p_obj = Product(**info)
                    p_obj.save()
