import scrapy
from ..items import Earphone

class AmazonScraper(scrapy.Spider):
    name = "amazEarphones"

    # How many pages you want to scrape
    no_of_pages = 1

    # Headers to fix 503 service unavailable error
    # Spoof headers to force servers to think that request coming from browser ;)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0'}

    def start_requests(self):
        # starting urls for scraping
        urls = [
            "https://www.amazon.in/s?k=earphones&i=computers&ref=nb_sb_noss_2",
            "https://www.amazon.in/s?k=earphones&i=computers&page=2&qid=1595754535&ref=sr_pg_2",
            "https://www.amazon.in/s?k=earphones&i=computers&page=3&qid=1595754560&ref=sr_pg_3",
            "https://www.amazon.in/s?k=earphones&i=computers&page=4&qid=1595754578&ref=sr_pg_4",
            "https://www.amazon.in/s?k=earphones&i=computers&page=5&qid=1595754592&ref=sr_pg_5"
        ]

        for url in urls: yield scrapy.Request(url = url, callback = self.parse, headers = self.headers)

    def parse(self, response):

        self.no_of_pages -= 1

        # print(response.text)

        earphones = response.xpath("//a[@class='a-link-normal a-text-normal']").xpath("@href").getall()
        
        # print(len(mobiles))

        for ep in earphones:
            final_url = response.urljoin(ep)
            yield scrapy.Request(url=final_url, callback = self.parse_ep, headers = self.headers)
            # break
            # print(final_url)

        # print(response.body)
        # product_name = response.xpath("//span[@class='a-size-medium a-color-base a-text-normal']//text()").getall()
        # product_name = response.css('span').getall()
        # print(product_name)
        
        if(self.no_of_pages > 0):
            next_page_url = response.xpath("//ul[@class='a-pagination']/li[@class='a-last']/a").xpath("@href").get()
            final_url = response.urljoin(next_page_url)
            yield scrapy.Request(url = final_url, callback = self.parse, headers = self.headers)

    def parse_ep(self, response):
        product_name = response.xpath("//span[@id='productTitle']//text()").get() or response.xpath("//h1[@id='title']//text()").get()
        #brand = response.xpath("//a[@id='bylineInfo']//text()").get() or "not specified"
        rating = response.xpath("//div[@id='averageCustomerReviews_feature_div']").xpath("//span[@class='a-icon-alt']//text()").get()

        price = response.xpath("//span[@id='priceblock_ourprice']//text()") or response.xpath("//span[@id='priceblock_dealprice']//text()")
        print(price)
        if len(price) > 1: price = price[1].get()
        elif len(price) == 1: price = price[0].get()
        else : price = price.get()

        #colour = response.xpath("//div[@id='variation_color_name']/div/span[@class='selection']//text()").get() or "not defined"
        instock = response.xpath("//div[@id='availability']").xpath("//span[@class='a-size-medium a-color-success']//text()").get() or "Out Stock"
        instock = instock.strip() == "In stock."
        description_raw = response.xpath("//div[@id='featurebullets_feature_div']//span[@class='a-list-item']//text()").getall()
        asin = response.xpath("//*[@id='prodDetails']/div[2]/div[2]/div[1]/div[2]/div/div/table/tbody/tr[1]/td[2]//text()").extract() or response.xpath("//*[@id='prodDetails']/div/div[2]/div[1]/div[2]/div/div/table/tbody/tr[1]/td[2]//text()").extract()
        img_url = response.xpath("//img[@id='landingImage']/@data-old-hires").get() or response.xpath("//img[@id='imgBlkFront']/@src").get()
        category = 'Earphones and Headphones'
        description = []
        for description_temp in description_raw:
            description.append(description_temp.strip())

        print(product_name, asin, rating, price, instock, img_url)
        # print(description)
        #instock = instock,
        # brand = brand.strip(),
        #description = description,

        yield Earphone(product_name = product_name.strip(), asin = asin, rating = rating.strip(), price = price.strip(), category = category  ,description = description, image_urls = [img_url])