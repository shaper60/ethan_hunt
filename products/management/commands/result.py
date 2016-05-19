# coding: utf-8
import time
import json
import csv

from django.core.management.base import BaseCommand, CommandError

from products.models import Product, Maker


class Command(BaseCommand):
    def handle(self, *args, **options):

        timestr = time.strftime("%Y%m%d%H%M%S")
        with open('products/results/result_%s.csv' % timestr, 'w') as f:
            writer = csv.writer(f)

            writer.writerow(['product_count', 'jancode_count', 'releasedate_count', 'manual_count'])

            product_list = Product.objects.all()
            jancode_list = Product.objects.exclude(jancode='').all()
            releasedate_list = Product.objects.exclude(releasedate=None).all()
            manual_list = Product.objects.exclude(manual='').all()
            writer.writerow([len(product_list), len(jancode_list), len(releasedate_list), len(manual_list)])

            writer.writerow('')

            writer.writerow(['maker_name', 'product_count', 'manual_count'])

            maker_list = Maker.objects.all()
            for maker in maker_list:
                product_list = Product.objects.filter(maker=maker).all()
                if product_list:
                    manual_list = Product.objects.filter(maker=maker).exclude(manual='').all()
                    print(maker.name)
                    print(len(product_list), len(manual_list))
                    writer.writerow([maker.name.encode('utf-8'), len(product_list), len(manual_list)])
