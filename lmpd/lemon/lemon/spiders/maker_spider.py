import scrapy
import lxml.etree
import js2xml
import lmpd.lemon.lemon.items as lmpd
from scrapy.loader import ItemLoader

class MakerSpider(scrapy.Spider):
    name = 'makerspider'
    allowed_domains = ['autoscout24.de']
    start_urls = ['http://autoscout24.de/']

    custom_settings = {
        'ITEM_PIPELINES': {
            'lmpd.lemon.lemon.pipelines.MakersPipeline': 100
        }
    }

    def parse(self, response):
        script = response.xpath("//script[contains(text(), 'window.As24HomeTabsConfig')]/text()").extract_first()
        xml = lxml.etree.tostring(js2xml.parse(script), encoding='unicode')
        selector = scrapy.Selector(text=xml)
        all_makers = selector.css('property[name="allMakes"]>array>object')
        for maker in all_makers:
            l = ItemLoader(item=lmpd.MakerItem(), selector=maker)
            l.add_css('id', 'property[name="id"] > string')
            l.add_css('name', 'property[name="label"] > string')
            l.add_css('is_top', 'boolean')
            yield l.load_item()