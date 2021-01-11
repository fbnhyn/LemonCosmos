from lmpd.lemon.lemon.items import LemonItem
from urllib.parse import urljoin
import scrapy
import math
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class LemonSpider(CrawlSpider):
    name = 'lemonspider'
    allowed_domains = ['autoscout24.de']

    rules = [
        Rule(LinkExtractor(allow='angebote/', deny='leasing'), callback='parse_filter_lemon', follow=True),
    ]

    def parse_filter_lemon(self, response):
        if (response.css('.cldt-item[data-item-name="car-details"]')):
            # TODO: load car lemon item
            pass