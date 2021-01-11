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
            query_result_hits = int(response.css('.cl-filters-summary-counter::text').extract_first().replace('.', ""))
            self.combind_query_counter += query_result_hits
            print(f'Evaluate {response}\nHits: {query_result_hits}\nCounter: {self.combind_query_counter}')
            if (query_result_hits == 0):
                print('No Query Results')
            elif (query_result_hits > 200):
                yield scrapy.Request(response.url, callback=self.refine_query)
            else:
                pages = math.ceil((query_result_hits / 10) + 1)
                for p in range(1, pages):
                    self.query_urls.append(response.url + f'&?page={p}')
        except AttributeError:
            print(f"Reloading Query again {response}")
            yield scrapy.Request(response.url, callback=self.parse, dont_filter=True)
        except:
            e = sys.exc_info()[0]
            print(f'{e.__class__} for {response}')

    def refine_query(self, response):
        print('Refine query')
        print(response)