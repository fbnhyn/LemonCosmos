from itemadapter.adapter import ItemAdapter
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
        
        # create result dict containing all models for one maker
        # in order to be able to update the maker later, the makerid must be part of the result dict
        result = {
            'maker_id': selector.css('property[name="makeId"] > string::text').extract_first(),
            'models': []
        }
        for raw_model in models:
            # only queryable models are extracted and persisted in the database
            if (raw_model.css('property[name="isModel"] > boolean::text').extract_first() == 'true'):
                l = ItemLoader(item=lmpd.ModelItem(), selector=raw_model)
                l.add_css('id', 'property[name="id"] > string')
                l.add_css('name', 'property[name="name"] > string')
                result['models'].append(ItemAdapter(l.load_item()).asdict())
        return result