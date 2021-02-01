from datetime import datetime
from lmpd.lemon.lemon.items import AdressItem, LemonItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader

class LemonSpider(CrawlSpider):
    name = 'lemonspider'
    allowed_domains = ['autoscout24.de']

    rules = [
        Rule(LinkExtractor(allow='angebote/', deny='leasing'), callback='parse_lemon', follow=True),
    ]

    def parse_lemon(self, response):
        if (response.css('.cldt-item[data-item-name="car-details"]')):
            l = ItemLoader(item=LemonItem(), selector=response)
            l.add_css('id', "[as24-tracking-value*='classified_productGuid']::attr('as24-tracking-value')")
            l.add_css('origin', "[as24-tracking-value*='classified_oigin']::attr('as24-tracking-value')")
            l.add_css('fuel_type', "[as24-tracking-value*='fuel_type']::attr('as24-tracking-value')")
            l.add_css('makeId', "[as24-tracking-value*='classified_makeId']::attr('as24-tracking-value')")
            l.add_css('makeName', "[as24-tracking-value*='classified_makeTxt']::attr('as24-tracking-value')")
            l.add_css('modelId', "[as24-tracking-value*='classified_modelID']::attr('as24-tracking-value')")
            l.add_css('modelName', "[as24-tracking-value*='classified_modelTxt']::attr('as24-tracking-value')")
            l.add_css('power', "[as24-tracking-value*='classified_power']::attr('as24-tracking-value')")
            l.add_css('price', "[as24-tracking-value*='classified_price']::attr('as24-tracking-value')")
            l.add_css('offer_type', "[as24-tracking-value*='classified_offerType']::attr('as24-tracking-value')")
            l.add_css('segment', "[as24-tracking-value*='classified_carSegment']::attr('as24-tracking-value')")
            l.add_css('year', "[as24-tracking-value*='classified_year']::attr('as24-tracking-value')")
            l.add_css('milage', "[as24-tracking-value*='classified_mileage']::attr('as24-tracking-value')")
            l.add_value('adress', self.parse_adress(response))
            l.add_value('crawled', datetime.now().time())
            yield l.load_item()

    def parse_adress(self, response):
        a = ItemLoader(item=AdressItem(), selector=response)
        a.add_css('city', '[data-item-name=vendor-contact-city]::text')
        a.add_css('area_code', "[as24-tracking-value*='classified_zipcode']::attr('as24-tracking-value')")
        a.add_css('country', "[as24-tracking-value*='classified_country']::attr('as24-tracking-value')")
        return a.load_item()