from lmpd.lemon.lemon import models
import scrapy
import math
import sys

class QuerySpider(scrapy.Spider):
    name = 'querySpider'
    allowed_domains = ['autoscout24.de']
    result = models.QueryResult()

    def parse(self, response):
        try:
            query_hits = int(response.css('.cl-filters-summary-counter::text').extract_first().replace('.', ""))
            q = models.Query(response, query_hits)
            if query_hits > 200:
                yield scrapy.Request(q.refine_query(), callback=self.parse, dont_filter=True)
            elif query_hits < 200:
                self.result.hits += query_hits
                pages = math.ceil((query_hits / 20) + 1)
                for p in range(1, pages):
                    self.result.urls.append(response.url + f'&page={p}')
                if q.has_upper_query:
                    yield scrapy.Request(q.refine_query(), callback=self.parse, dont_filter=True)
        except AttributeError:
            yield scrapy.Request(response.url, callback=self.parse, dont_filter=True)
        except:
            e = sys.exc_info()
            print(f'EXCEPTION {e[1]}')