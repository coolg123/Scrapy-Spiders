import scrapy


# class EhentaiSpider(scrapy.Spider):
#     name = "ehentai"
#     allowed_domains = ["e-hentai.org"]
#     start_urls = ["https://e-hentai.org/g/2260549/885dd7f58b"]

class EhentaiSpider(scrapy.Spider):
    name = "ehentai"
    allowed_domains = ["e-hentai.org"]

    def __init__(self, start_url=None, *args, **kwargs):
        super(EhentaiSpider, self).__init__(*args, **kwargs)
        self.start_urls = [start_url] if start_url else []

    def parse(self, response):
        values = response.xpath('//div[@id="gdt"]/div/div/a')
        for links in values:
            link = links.xpath('.//@href').get()
            yield response.follow(link, callback=self.parse_image)
        
        next_page = response.xpath('//div[@class="gtb"][1]/table/tr/td/a[contains(text(), ">")]/@href').get()
        
        if next_page:
            yield response.follow(next_page, callback=self.parse)
    
    def parse_image(self, response): # yeha hum image download karenge
        image = response.xpath('//div[@id="i3"]/a/img/@src').get()
        count = response.xpath('//div[@id="i2"]/div/div/span/text()').get()
        yield {
            'number': count,
            'image_urls': [image]
        }
