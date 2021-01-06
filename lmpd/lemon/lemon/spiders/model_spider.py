import scrapy


class ModelSpider(scrapy.Spider):
    name = 'modelspider'
    allowed_domains = ['autoscout24.de']
    start_urls = ['http://autoscout24.de/']

    def parse(self, response):
        pass
