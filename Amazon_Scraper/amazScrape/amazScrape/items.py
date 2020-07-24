# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst
from w3lib.html import remove_tags


class amazScrapeItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    prodName = scrapy.Field(
        input_processor = MapCompose(remove_tags),
        output_processor = TakeFirst()

    )
    prodPrice = scrapy.Field()
    
class Mobile(scrapy.Item):
    title = scrapy.Field()
    rating = scrapy.Field()
    price = scrapy.Field()
    colour = scrapy.Field()
    instock = scrapy.Field()
    description = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
    asin = scrapy.Field()
    
