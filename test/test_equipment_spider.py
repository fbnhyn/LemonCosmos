import unittest
from pprint import pprint
from scrapy.http.response.text import TextResponse

from lmpd.lemon.lemon.spiders.equipment_spider import EquipmentSpider

class TestEquipmentSpider(unittest.TestCase):

    def setUp(self):
        self.spider = EquipmentSpider(limit=1)
        
        self.response = TextResponse(
            url='www.filterunittest.de',
            body=open(f'tmp\\filter.equipments.htm', encoding='utf-8').read(),
            encoding = 'utf-8'
        )

    def test_parse_equipment(self):
        result = self.spider.parse_equipment(self.response)
        sr = sorted(list(result), key=lambda e: e.get('id'), reverse=False)
        pprint(sr)

if __name__ == '__main__':
    unittest.main()