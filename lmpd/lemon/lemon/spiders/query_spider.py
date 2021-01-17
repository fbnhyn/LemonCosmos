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
                print(f'refing query for {response.url}; {query_hits}')
                yield scrapy.Request(q.refine_query(), callback=self.parse, dont_filter=True)
            elif query_hits > 0 and query_hits <= 200:
                self.result.hits += query_hits
                if query_hits > 20:
                    pages = math.ceil((query_hits / 20)) + 1
                    for p in range(1, pages):
                        print(f'adding {response.url}&page={p}')
                        self.result.urls.append(response.url + f'&page={p}')
                else:
                    print(f'adding {response.url}')
                    self.result.urls.append(response.url)
                print(f'result_hits: {self.result.hits} ({len(self.result.urls)})')
                if q.has_upper_query:
                    yield scrapy.Request(q.refine_query(), callback=self.parse, dont_filter=True)
        except AttributeError:
            yield scrapy.Request(response.url, callback=self.parse, dont_filter=True)
        except:
            e = sys.exc_info()
            print(f'EXCEPTION {e[1]}')