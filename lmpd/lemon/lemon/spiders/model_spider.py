import scrapy
import lxml.etree
import js2xml
import lmpd.lemon.lemon.items as lmpd
from scrapy.loader import ItemLoader

class ModelSpider(scrapy.Spider):
    name = 'modelspider'
    allowed_domains = ['autoscout24.de']

    custom_settings = {
        'ITEM_PIPELINES': {
            'lmpd.lemon.lemon.pipelines.ModelsPipeline': 100
        }
    }

    def parse(self, response):
        script = response.xpath("//script[contains(text(), 'window.As24ClassifiedList')]/text()").extract_first()
        xml = lxml.etree.tostring(js2xml.parse(script), encoding='unicode')
        selector = scrapy.Selector(text=xml)
        models = selector.css('property[name="availableModelModelLines"] > array > object')
        for model in models:
            if (model.css('property[name="isModel"] > boolean::text').extract_first() == 'true'):
                l = ItemLoader(item=lmpd.ModelItem(), selector=model)
                l.add_css('id', 'property[name="id"] > string')
                l.add_css('name', 'property[name="name"] > string')
                l.add_value('makerId', selector.css('property[name="makeId"] > string::text').extract_first())
                yield l.load_item()
