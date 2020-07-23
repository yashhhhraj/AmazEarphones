# -*- coding: utf-8 -*-
import scrapy
from ..items import amazScrapeItem


class AmazearphonesSpider(scrapy.Spider):
    name = 'amazEarphones'
    start_urls = [
        'https://www.amazon.in/s?k=earphones&ref=nb_sb_noss_2'
        ]

    def parse(self, response):
        items = amazScrapeItem()

        prodName = response.css('.a-text-normal .a-text-normal').css('::text').extract

        prodPrice = response.css('.sg-col-24-of-28+ .sg-col-24-of-28 .a-size-base.a-color-secondary > span span , .a-price-whole').css('::text').extract

        items['prodName'] = prodName
        items['prodPrice'] = prodPrice

        yield items