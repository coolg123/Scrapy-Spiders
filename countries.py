import scrapy


class CountriesSpider(scrapy.Spider):
    name = "countries"
    allowed_domains = ["www.worldometers.info"]
    start_urls = ["https://www.worldometers.info/population/"]

    def parse(self, response):
        title = response.xpath('//div[@class="content-inner"]/h2[3]/text()').get()
        countries = response.xpath('//div[@class="content-inner"]/ul[8]/li/a/text()').getall()
        links = response.xpath('//div[@class="content-inner"]/ul[8]/li/a')

        for link in links:
            country_name = link.xpath('.//text()').get()
            country_link = link.xpath('.//@href').get()

            # To create absolute url from relative url and pass it to scrapy.Request()
            # absolute_url = 'https://www.worldometers.info' + country_link
            # absolute_url = response.urljoin(country_link)
            # yield scrapy.Request(url=absolute_url)

            # To follow next link without creating absolute url , just pass relative url to response.follow()
            yield response.follow(url=country_link, callback=self.parse_countries, meta={'country_name': country_name})
        
            # yield {
            #     "country-name": country_name,
            #     "country-link": 'https://www.worldometers.info' + country_link
            # }

    def parse_countries(self, response):

        country_name = response.request.meta['country_name']
        rows = response.xpath('//div[@class="table-responsive"]/table/tbody/tr')

        for row in rows:
            year = row.xpath('.//td[1]/text()').get()
            population = row.xpath('.//td[2]/strong/text()').get()

            yield {
                "country_name": country_name,
                "year": year,
                "population": population
            }


