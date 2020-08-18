# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst
from w3lib.html import remove_tags


class Electr(scrapy.Item):
    ims = scrapy.Field()
    stores = scrapy.Field()
    iurl = scrapy.Field()
    category = scrapy.Field()
    subcategory = scrapy.Field()
    product_name = scrapy.Field()
    rating = scrapy.Field()
    price = scrapy.Field()
    colour = scrapy.Field()
    instock = scrapy.Field()
    description = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
    asin = scrapy.Field()
    product_id = scrapy.Field()
