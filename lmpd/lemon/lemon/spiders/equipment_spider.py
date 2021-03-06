from re import I
import scrapy
from lmpd.lemon.lemon.items import EquipmentItem
from scrapy.item import Item
from scrapy.loader import ItemLoader

class EquipmentSpider(scrapy.Spider):
    name = 'equipmentSpider'

    def parse_equipment(self, response):
        equipment_nodes = response.css('.cl-equipment')
        for equipment in equipment_nodes:
            l = ItemLoader(item=EquipmentItem(), selector=equipment)
            l.add_css('id', '.cl-equipment::attr("data-test")')
            l.add_css('name', 'label')
            yield l.load_item()