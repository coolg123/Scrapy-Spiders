import scrapy


class Way2fresherSpider(scrapy.Spider):
    name = "way2fresher"
    allowed_domains = ["way2fresher.com"]
    start_urls = ["https://way2fresher.com/jobs"]

    def parse(self, response):

        for job in response.xpath('//h2[@class="job-title"]'):
            # follow link to job page
            page_url = job.xpath('.//a/@href').get()
            yield response.follow(page_url, self.parse_job)

        # follow pagination link
        next_page = response.xpath('//a[@class="next page-numbers"]/@href').get()

        if next_page:
            yield response.follow(next_page, self.parse)

    def parse_job(self, response):
        yield {
            'Title': response.xpath('//h3[@class="employer-title"]/text()').get(),
            'Location': response.xpath('//div[@class="job-location with-icon"]/text()').get(),
            'Experience': response.xpath("//strong[normalize-space()='Experience :']/parent::p/text()").get(),

            "Apply-Link": response.xpath("//div[@class='action hidden-lg hidden-md']//a[@class='btn btn-apply btn-apply-job-external'][normalize-space()='Apply Now']/@href").get(),
        }
        
