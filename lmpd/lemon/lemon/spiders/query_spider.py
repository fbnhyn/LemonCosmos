import sys
import scrapy
import logging
import math
import traceback

from scrapy.http.response.text import TextResponse
from lmpd.lemon.lemon import models

class QuerySpider(scrapy.Spider):
    name = 'QuerySpider'
    allowed_domains = ['autoscout24.de']
    result = models.QueryResult()

    custom_settings = {
        'CONCURRENT_REQUESTS': 64
    }

    def __init__(self, *a, **kw):
        self.logger.setLevel(logging.INFO)
        super().__init__(*a, **kw)

    def parse(self, response: TextResponse):
        try:
            query = models.Query(response, self.parse_query_result(response))
            self.logger.info(f'{query.hits: < 10} by {response.url}')
            if (query.hits == 0 and query.price_from is None and query.price_to is None): return
            elif (query.hits == 0): yield scrapy.Request(query.refine(), callback=self.parse, dont_filter=True)
            elif (query.hits > query.hit_cap): yield scrapy.Request(query.refine(), callback=self.parse, dont_filter=True)
            else:
                self.result.hits += query.hits
                self.add_query(response, query)
                self.logger.info(f'{self.result.hits: < 10} hits in total')
                if query.has_upper(): yield scrapy.Request(query.refine(), callback=self.parse, dont_filter=True)
        except AttributeError:
            self.logger.warn(f'{response.url} did not contain any valid html')
            yield scrapy.Request(response.url, callback=self.parse, dont_filter=True)
        except:
            self.logger.error(traceback.format_exc())

    def parse_query_result(self, response: TextResponse):
        hasEmptyTitleClass = len(response.css('.cl-list-header-title-empty')) > 0
        if (hasEmptyTitleClass): return 0
        return int(response.css('.cl-filters-summary-counter>span::text').extract_first().replace('.', ""))

    def add_query(self, response: TextResponse, query: models.Query):
        if (query.hits > 20): self.add_query_pagination(response, query)
        else: self.result.urls.append(response.url)

    def add_query_pagination(self, response: TextResponse, query: models.Query):
        pages = math.ceil((query.hits / 20)) + 1
        for p in range(1, pages):
            self.result.urls.append(response.url + f'&page={p}')