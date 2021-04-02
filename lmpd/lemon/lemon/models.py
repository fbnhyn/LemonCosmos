from datetime import datetime
import logging
import math
from urllib import parse

import scrapy.http

class Query:
    max_price = 999999999
    min_price = 0
    first_price_cap = 12500
    hit_cap = 400
    
    def __init__(self, response: scrapy.http.Response, hits: int):
        self.response:scrapy.http.Response = response
        self.parsed_url = parse.urlparse(response.url)
        self.query = parse.parse_qs(self.parsed_url.query)
        self.price_from: int = int(self.query.get('pricefrom')[0]) if self.query.get('pricefrom') is not None else None
        self.price_to: int = int(self.query.get('priceto')[0]) if self.query.get('priceto') is not None else None
        self.hits: int = hits

    def refine(self):
        if self.price_from is None and self.price_to is None:
            self.query['pricefrom'] = [str(self.min_price)]
            self.query['priceto'] = [str(self.first_price_cap)]
            return self.__compose_new_url()
        if self.hits > self.hit_cap:
            return self.__refine_lower_query()
        return self.__refine_upper_query()

    def has_upper(self):
        if self.price_to is None and self.hits <= 200:
            return False
        if self.price_to == self.max_price:
            return False
        return True

    def __refine_lower_query(self):
        if self.price_to is None:
            if self.price_from is not None:
                self.query['priceto'] = [str(self.price_from * 5)]
            else:
                self.query['priceto'] = ['100000']
        else:
            price_range = self.price_to - self.price_from
            divider = self.__get_divider(price_range)
            self.query['priceto'] = [str(math.floor((self.price_from + self.price_to) / divider))]
        return self.__compose_new_url()

    def __refine_upper_query(self):
        if self.price_to is None:
            self.query['pricefrom'] = [str(self.price_from * 5)]
        else:
            self.query['pricefrom'] = [str(self.price_to + 1)]
            self.query.pop('priceto')
        return self.__compose_new_url()

    def __get_divider(self, price_range: int):
        if price_range > 500000:
            return 8
        if price_range > 100000:
            return 4
        return 2

    def __compose_new_url(self):
        self.parsed_url = self.parsed_url._replace(query=parse.urlencode(self.query, doseq=True))
        return parse.urlunparse(self.parsed_url)

class QueryResult:
    urls: list
    hits: int
    time: datetime