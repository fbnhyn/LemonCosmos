import math
from urllib import parse

import scrapy.http

class Query:
    max_price = 999999999
    min_price = 0
    first_price_cap = 12500
    hit_cap = 200
    
    def __init__(self, response: scrapy.http.Response, hits: int):
        self.response:scrapy.http.Response = response
        self.components = dict(parse.parse_qsl(parse.urlsplit(response.url).query))
        self.price_from: int = self.__get_component_param_as_int('pricefrom')
        self.price_to: int = self.__get_component_param_as_int('priceto')
        self.country: str = self.components.get('cy')
        self.offer: str = self.components.get('offer')
        self.hits: int = hits
        self.has_upper_query: bool = self.__has_upper_query()

    def refine_query(self):
        if self.price_from is None and self.price_to is None:
            self.price_from = self.min_price
            self.price_to = self.first_price_cap
            return self.response.urljoin(f'?offer{self.offer}&cy={self.country}&pricefrom={self.price_from}&priceto={self.price_to}')
        if self.hits > self.hit_cap:
            return self.__refine_lower_query()
        return self.__refine_upper_query()

    def __has_upper_query(self):
        return False if self.price_to is None or self.price_to == self.max_price else True

    def __replace_param_in_url(self, url, param, old_value, new_value):
        return url.replace(f'{param}={old_value}', f'{param}={new_value}')

    def __refine_lower_query(self):
        price_range = self.price_to - self.price_from
        divider = self.__get_divider(price_range)
        new_price_to = math.floor((self.price_from + self.price_to) / divider)
        return self.__replace_param_in_url(self.response.url, 'priceto', self.price_to, new_price_to)

    def __refine_upper_query(self):
        new_price_from = self.price_to + 1
        new_price_to = self.max_price
        new_url = self.__replace_param_in_url(self.response.url, 'pricefrom', self.price_from, new_price_from)
        new_url = self.__replace_param_in_url(new_url, 'priceto', self.price_to, new_price_to)
        return new_url

    def __get_component_param_as_int(self, param: str):
        query_param = self.components.get(param)
        return None if query_param is None else int(query_param)

    def __get_divider(self, price_range: int):
        if price_range > 500000:
            return 8
        if price_range > 100000:
            return 4
        return 2
