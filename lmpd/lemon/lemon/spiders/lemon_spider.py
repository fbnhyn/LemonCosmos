import scrapy

class Spider(scrapy.Spider):
    name = 'lemonspider'
    allowed_domains = ['autoscout24.de']
    start_urls = ['http://autoscout24.de/']

    def parse(self, response):
        pass
