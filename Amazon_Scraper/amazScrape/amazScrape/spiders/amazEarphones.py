import scrapy
from ..items import amazScrapeItem
from scrapy.loader import ItemLoader

class AmazearphonesSpider(scrapy.Spider):
    name = 'amazEarphones'
    start_urls = [
        'https://www.amazon.in/s?k=earphones&ref=nb_sb_noss',
        'https://www.amazon.in/s?k=earphones&page=2&qid=1595577590&ref=sr_pg_2',
        'https://www.amazon.in/s?k=earphones&page=2&qid=1595577590&ref=sr_pg_3',
        'https://www.amazon.in/s?k=earphones&page=2&qid=1595577590&ref=sr_pg_4',
        'https://www.amazon.in/s?k=earphones&page=2&qid=1595577590&ref=sr_pg_5',
        'https://www.amazon.in/s?k=earphones&page=2&qid=1595577590&ref=sr_pg_6',
        'https://www.amazon.in/s?k=earphones&page=2&qid=1595577590&ref=sr_pg_7',
        'https://www.amazon.in/s?k=earphones&page=2&qid=1595577590&ref=sr_pg_8',
        'https://www.amazon.in/s?k=earphones&page=2&qid=1595577590&ref=sr_pg_9',
        'https://www.amazon.in/s?k=earphones&page=2&qid=1595577590&ref=sr_pg_10',
        
        ]

    def parse(self, response):
        items = amazScrapeItem()
        '''for i in response.xpath(".//span[@class='a-size-medium a-color-base a-text-normal']/text"):
            l = ItemLoader(item=amazScrapeItem(), selector= i)
            l.add_xpath('prodName',".//span[@class='a-size-medium a-color-base a-text-normal']/text")
            yield {
                'prodName': i.xpath(".//span[@class='a-size-medium a-color-base a-text-normal']/text").extract_first()
            }'''

        
        prodName = response.css('.sg-col-24-of-28~ .sg-col-24-of-28+ .sg-col-24-of-28 .a-size-medium.a-text-normal').css('::text').extract()
        
        prodPrice = response.css('.sg-col-24-of-28~ .sg-col-24-of-28+ .sg-col-24-of-28 .sg-row .a-price-whole').css('::text').extract()

        items['prodName'] = prodName
        items['prodPrice'] = prodPrice

        yield items