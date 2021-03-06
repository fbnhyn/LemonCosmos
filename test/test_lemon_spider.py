import unittest
from pprint import pprint
from scrapy.http.response.text import TextResponse

from lmpd.lemon.lemon.spiders.lemon_spider import LemonSpider

class TestLemonSpider(unittest.TestCase):

    def setUp(self):
        self.spider = LemonSpider(limit=1)

    def test_parse_dacia(self):
        self.response = TextResponse(
            url='www.lemonunittest.de',
            body=open(f'tmp\\dacia.sandero.htm', encoding='utf-8').read(),
            encoding = 'utf-8'
        )

        result = self.spider.parse_lemon(self.response)
        lemon =  next(result)
        pprint(lemon)

    def test_parse_volkswagen_passat(self):
        self.response = TextResponse(
            url='www.lemonunittest.de',
            body=open(f'tmp\\volkswagen.passat.htm', encoding='utf-8').read(),
            encoding = 'utf-8'
        )

        result = self.spider.parse_lemon(self.response)
        lemon =  next(result)
        pprint(lemon)

if __name__ == '__main__':
    unittest.main()