import unittest
from pprint import pprint
from scrapy.http.response.text import TextResponse

from lmpd.lemon.lemon.spiders.lemon_spider import LemonSpider

class TestLemonSpider(unittest.TestCase):

    def setUp(self):
        self.spider = LemonSpider(limit=1)
        
        self.response = TextResponse(
            url='www.lemonunittest.de',
            body=open(f'tmp\\dacia.sandero.htm', encoding='utf-8').read(),
            encoding = 'utf-8'
        )

    def test_parse_lemon(self):
        result = self.spider.parse_lemon(self.response)
        for r in result:
            pprint(r)

if __name__ == '__main__':
    unittest.main()