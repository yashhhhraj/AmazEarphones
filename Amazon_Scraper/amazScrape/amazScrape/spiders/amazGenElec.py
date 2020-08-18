import scrapy, random, string
from ..items import Electr

class AmazonScraper(scrapy.Spider):
    name = "amazGenElec"

    # How many pages you want to scrape
    no_of_pages = 1

    # Headers to fix 503 service unavailable error
    # Spoof headers to force servers to think that request coming from browser ;)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0'}

    def start_requests(self):
        # starting urls for scraping
        urls = ["https://www.amazon.in/s?k=fitness+band&ref=nb_sb_noss_1",
                "https://www.amazon.in/s?k=smartwatch&ref=nb_sb_noss_2",
                "https://www.amazon.in/s?k=tv+stick&ref=nb_sb_noss_2",
                
                #"https://www.amazon.in/s?k=laptop&page=3&qid=1596551468&ref=sr_pg_3",
                #"https://www.amazon.in/s?k=laptop&page=4&qid=1596551492&ref=sr_pg_4",
                #"https://www.amazon.in/s?k=laptop&page=5&qid=1596551510&ref=sr_pg_5",
                #"https://www.amazon.in/s?k=laptop&page=6&qid=1596551527&ref=sr_pg_6",
                #"https://www.amazon.in/s?k=laptop&page=7&qid=1596551570&ref=sr_pg_7",
                #"https://www.amazon.in/s?k=laptop&page=8&qid=1596551595&ref=sr_pg_8",
                #"https://www.amazon.in/s?k=laptop&page=9&qid=1596551636&ref=sr_pg_9"
        ]

        for url in urls: yield scrapy.Request(url = url, callback = self.parse, headers = self.headers)


    def parse(self, response):

        self.no_of_pages -= 1

        # print(response.text)

        elecs = response.xpath("//a[@class='a-link-normal a-text-normal']").xpath("@href").getall()

        # print(len(mobiles))

        for elec in elecs:
            final_url = response.urljoin(elec)
            yield scrapy.Request(url=final_url, callback = self.parse_elec, headers = self.headers)
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

    def parse_elec(self, response):
        product_name = response.xpath("//span[@id='productTitle']//text()").get() or response.xpath("//h1[@id='title']//text()").get()
        #brand = response.xpath("//a[@id='bylineInfo']//text()").get() or "not specified"
        rating = response.xpath("//div[@id='averageCustomerReviews_feature_div']").xpath("//span[@class='a-icon-alt']//text()").get()

        price = response.xpath("//span[@id='priceblock_ourprice']//text()") or response.xpath("//span[@id='priceblock_dealprice']//text()")
        print(price)
        if len(price) > 1: price = price[1].get()
        elif len(price) == 1: price = price[0].get()
        else : price = price.get()
        asin = response.xpath("//*[@id='prodDetails']/div[2]/div[2]/div[1]/div[2]/div/div/table/tbody/tr[1]/td[2]//text()").extract() or response.xpath("//*[@id='prodDetails']/div/div[2]/div[1]/div[2]/div/div/table/tbody/tr[1]/td[2]//text()").extract()
        for i in asin:
            asin = ''
            asin+=i
        iurl = response.url
        stores = [{
            "storeProductId": asin,
            "storeLink": iurl,
            "storeName": "amazon",
            "storePrice": ''.join([c for c in price if c in '1234567890.'])[:-3]
        }]


        colour = response.xpath("//div[@id='variation_color_name']/div/span[@class='selection']//text()").get() or "not defined"
        instock = response.xpath("//div[@id='availability']").xpath("//span[@class='a-size-medium a-color-success']//text()").get() or "Out Stock"
        instock = instock.strip() == "In stock."
        description_raw = response.xpath("//div[@id='featurebullets_feature_div']//span[@class='a-list-item']//text()").getall()
        #asin = response.xpath("//*[@id='prodDetails']/div[2]/div[2]/div[1]/div[2]/div/div/table/tbody/tr[1]/td[2]//text()").extract() or response.xpath("//*[@id='prodDetails']/div/div[2]/div[1]/div[2]/div/div/table/tbody/tr[1]/td[2]//text()").extract()
        photos = response.xpath("//img[@id='landingImage']/@data-old-hires").get() or response.xpath("//img[@id='imgBlkFront']/@src").get()
        category = 'Electronics'
        subcategory = 'Others'
        description = ''

        for description_temp in description_raw:
            description += description_temp.strip() + ', '

        description = description[:-2]
        product_id = ''.join(random.sample(string.ascii_lowercase+string.digits,15)) #random 15 len alphanumeric id

        print(product_name, rating, price, colour, instock, photos)
        # print(description)
        # brand = brand.strip(),
        #iurl = iurl, asin = asin, price = ''.join([c for c in price if c in '1234567890.'])[:-3], colour = colour.strip(), instock = instock, rating = rating.strip(),
        pp = Electr( product_name = product_name.strip(),product_id = product_id ,stores = stores,category = category,subcategory = subcategory, description = description, image_urls = [photos])
        yield pp