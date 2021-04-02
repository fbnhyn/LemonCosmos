from scrapy.http.response.text import TextResponse
from lmpd.lemon.lemon import models
import scrapy
import logging
import math
import sys

class QuerySpider(scrapy.Spider):
    name = 'querySpider'
    allowed_domains = ['autoscout24.de']
    result = models.QueryResult()

    def parse(self, response):
        try:
            self.logger.info(response.url)
            query = models.Query(response, self.parse_query_result(response))
            print(f'{query.hits}\tby {response.url}')
            if (query.hits == 0): return 
            if (query.hits > query.hit_cap): yield scrapy.Request(query.refine(), callback=self.parse, dont_filter=True)
            else:
                self.result.hits += query.hits
                self.add_query(response, query)
                print(f'[{self.result.hits}]')
                if query.has_upper(): yield scrapy.Request(query.refine(), callback=self.parse, dont_filter=True)
        except AttributeError:
            yield scrapy.Request(response.url, callback=self.parse, dont_filter=True)
        except:
            e = sys.exc_info()
            print(f'EXCEPTION {e[1]}')

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