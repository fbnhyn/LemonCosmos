from lmpd.lemon.lemon import models
import scrapy
import math
import sys

class QuerySpider(scrapy.Spider):
    name = 'querySpider'
    allowed_domains = ['autoscout24.de']
    combind_query_counter = 0
    query_urls = []

    def get_combind_query_counter(self):
        return self.combind_query_counter

    def parse(self, response):
        try:
            query_hits = int(response.css('.cl-filters-summary-counter::text').extract_first().replace('.', ""))
            print(f'Evaluate {response}\nHits: {query_hits}')
            q = models.Query(response, query_hits)
            if (query_hits == 0):
                print('No Query Results')
            elif (query_hits > 200):
                yield scrapy.Request(q.refine_query(), callback=self.parse, dont_filter=True)
            else:
                self.combind_query_counter += query_hits
                print(f'Combined Counter: {self.combind_query_counter}')
                
                pages = math.ceil((query_hits / 10) + 1)
                for p in range(1, pages):
                    self.query_urls.append(response.url + f'&page={p}')

                if q.has_upper_query:
                    yield scrapy.Request(q.refine_query(), callback=self.parse, dont_filter=True)

        except AttributeError:
            print(f"Reloading Query again {response}")
            yield scrapy.Request(response.url, callback=self.parse, dont_filter=True)
        except:
            e = sys.exc_info()
            print(f'EXCEPTION {e[1]}')