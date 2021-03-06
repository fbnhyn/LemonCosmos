from datetime import datetime
from lmpd.lemon.lemon.items import AdressItem, EmissionItem, LemonItem, PriceLabelRangesItem, PriceRangeItem
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
            l.add_css('origin', "[as24-tracking-value*='classified_origin']::attr('as24-tracking-value')")
            l.add_css('fuel_type', "[as24-tracking-value*='fuel_type']::attr('as24-tracking-value')")
            l.add_css('makeId', "[as24-tracking-value*='classified_makeId']::attr('as24-tracking-value')")
            l.add_css('makeName', "[as24-tracking-value*='classified_makeTxt']::attr('as24-tracking-value')")
            l.add_css('modelId', "[as24-tracking-value*='classified_modelID']::attr('as24-tracking-value')")
            l.add_css('modelName', "[as24-tracking-value*='classified_modelTxt']::attr('as24-tracking-value')")
            l.add_css('power', "[as24-tracking-value*='classified_power']::attr('as24-tracking-value')")
            l.add_css('price', "[as24-tracking-value*='classified_price\":']::attr('as24-tracking-value')")
            l.add_css('price_label', "[as24-tracking-value*='classified_pricelabel']::attr('as24-tracking-value')")
            l.add_css('offer_type', "[as24-tracking-value*='classified_offerType']::attr('as24-tracking-value')")
            l.add_css('segment', "[as24-tracking-value*='classified_carSegment']::attr('as24-tracking-value')")
            l.add_css('year', "[as24-tracking-value*='classified_year']::attr('as24-tracking-value')")
            l.add_css('milage', "[as24-tracking-value*='classified_mileage']::attr('as24-tracking-value')")
            l.add_css('equipment_codes', "[as24-tracking-value*='classified_equipment']::attr('as24-tracking-value')")
            l.add_css('doors', "[as24-tracking-value*='classified_doors']::attr('as24-tracking-value')")
            l.add_css('seats', "[as24-tracking-value*='classified_seats']::attr('as24-tracking-value')")
            l.add_css('consumption', "[as24-tracking-value*='classified_consumption']::attr('as24-tracking-value')")
            l.add_css('capacity', "[as24-tracking-value*='classified_capacity']::attr('as24-tracking-value')")
            l.add_css('is_superdeal', "[as24-tracking-value*='classified_superDealVehicle']::attr('as24-tracking-value')")
            l.add_css('equipment', '.cldt-item[data-item-name*="equipments"] * span')
            l.add_value('price_label_ranges', self.parse_price_label_ranges(response))
            l.add_value('emissions', self.parse_emssions(response))
            l.add_value('adress', self.parse_adress(response))
            l.add_value('crawled', datetime.now().time())
            yield l.load_item()

    def parse_adress(self, response):
        a = ItemLoader(item=AdressItem(), selector=response)
        a.add_css('city', '[data-item-name=vendor-contact-city]::text')
        a.add_css('area_code', "[as24-tracking-value*='classified_zipcode']::attr('as24-tracking-value')")
        a.add_css('country', "[as24-tracking-value*='classified_country']::attr('as24-tracking-value')")
        return a.load_item()

    def parse_emssions(self, response):
        e = ItemLoader(item=EmissionItem(), selector=response)
        e.add_css('co2', "[as24-tracking-value*='classified_emission\":']::attr('as24-tracking-value')")
        e.add_css('standard', "[as24-tracking-value*='classified_emissionStandard']::attr('as24-tracking-value')")
        return e.load_item()

    def parse_price_label_ranges(self, response):
        ul = response.css('ul.pe-visualization__bar')
        if (ul):
            l = ItemLoader(item=PriceLabelRangesItem(), selector=ul)
            l.add_value('top', self.parse_price_label_range_item(ul.css('li')[0]))
            l.add_value('good', self.parse_price_label_range_item(ul.css('li')[1]))
            l.add_value('fair', self.parse_price_label_range_item(ul.css('li')[2]))
            l.add_value('somewhat', self.parse_price_label_range_item(ul.css('li')[3]))
            l.add_value('expensiv', self.parse_price_label_range_item(ul.css('li')[4]))
            return l.load_item()

    def parse_price_label_range_item(self, price_range_node):
        r = ItemLoader(item=PriceRangeItem(), selector=price_range_node)
        r.add_css('start', 'span')
        r.add_css('end', 'span')
        return r.load_item()