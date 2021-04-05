import logging
import sys
import traceback

from lmpd.lemon.lemon.items import AdressItem, ConsumptionItem, EmissionItem, LemonItem, PriceLabelRangesItem, PriceRangeItem
from datetime import datetime
from scrapy.http.response.text import TextResponse
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader

class LemonSpider(CrawlSpider):
    name = 'lemonspider'
    allowed_domains = ['autoscout24.de']

    custom_settings = {
        'ITEM_PIPELINES': {
            'lmpd.lemon.lemon.pipelines.LemonPipeline': 100
        },
        'LOG_FILE' : '..\\..\\Logs\\lemons.log',
        'CONCURRENT_REQUESTS': 64
    }

    rules = [
        Rule(LinkExtractor(allow='angebote/', deny='leasing'), callback='parse_lemon', follow=False),
    ]

    def __init__(self, *a, **kw):
        self.logger.setLevel(logging.INFO)
        super().__init__(*a, **kw)

    def parse_lemon(self, response: TextResponse):
        try:
            if (response.status != 200): self.logger.error(f'{response.url} was {response.status}')
            elif (response.css('.cldt-item[data-item-name="car-details"]')):
                l = ItemLoader(item=LemonItem(), selector=response)
                l.add_css('id', "[as24-tracking-value*='classified_productGuid']::attr('as24-tracking-value')")
                l.add_css('origin', "[as24-tracking-value*='classified_origin']::attr('as24-tracking-value')")
                l.add_css('description', '.cldt-detail-version.sc-ellipsis')
                l.add_css('fuel_type', "[as24-tracking-value*='fuel_type']::attr('as24-tracking-value')")
                l.add_css('make_id', "[as24-tracking-value*='classified_makeId']::attr('as24-tracking-value')")
                l.add_css('make_name', "[as24-tracking-value*='classified_makeTxt']::attr('as24-tracking-value')")
                l.add_css('model_id', "[as24-tracking-value*='classified_modelID']::attr('as24-tracking-value')")
                l.add_css('model_name', "[as24-tracking-value*='classified_modelTxt']::attr('as24-tracking-value')")
                l.add_css('power', "[as24-tracking-value*='classified_power']::attr('as24-tracking-value')")
                l.add_css('price', "[as24-tracking-value*='classified_price\":']::attr('as24-tracking-value')")
                l.add_css('price_label', "[as24-tracking-value*='classified_pricelabel']::attr('as24-tracking-value')")
                l.add_css('pre_owners', "[as24-tracking-value*='classified_prevOwners']::attr('as24-tracking-value')")
                l.add_css('transmission', "[as24-tracking-value*='classified_transmission']::attr('as24-tracking-value')")
                l.add_css('offer_type', "[as24-tracking-value*='classified_offerType']::attr('as24-tracking-value')")
                l.add_css('segment', "[as24-tracking-value*='classified_carSegment']::attr('as24-tracking-value')")
                l.add_css('year', "[as24-tracking-value*='classified_year']::attr('as24-tracking-value')")
                l.add_css('milage', "[as24-tracking-value*='classified_mileage']::attr('as24-tracking-value')")
                l.add_css('equipment', '.cldt-item[data-item-name*="equipments"] * span')
                l.add_css('equipment_codes', "[as24-tracking-value*='classified_equipment']::attr('as24-tracking-value')")
                l.add_css('doors', "[as24-tracking-value*='classified_doors']::attr('as24-tracking-value')")
                l.add_css('seats', "[as24-tracking-value*='classified_seats']::attr('as24-tracking-value')")
                l.add_css('capacity', "[as24-tracking-value*='classified_capacity']::attr('as24-tracking-value')")
                l.add_css('is_superdeal', "[as24-tracking-value*='classified_superDealVehicle']::attr('as24-tracking-value')")
                l.add_value('fullservice', self.parse_exists_node_with_inner_html(response, "Scheckheftgepflegt"))
                l.add_value('fully_inspected', self.parse_exists_node_with_inner_html(response, "HU/AU neu"))
                l.add_value('warrenty', self.parse_exists_node_with_inner_html(response, "Garantie"))
                l.add_value('smoke_free', self.parse_exists_node_with_inner_html(response, "Nichtraucherfahrzeug"))
                l.add_value('lemon_condition', self.parse_definition_term("Zustand", response))
                l.add_value('weight', self.parse_definition_term("Leergewicht", response))
                l.add_value('body', self.parse_definition_term("Karosserieform", response))
                l.add_value('color', self.parse_definition_term("Außenfarbe", response))
                l.add_value('paint_type', self.parse_definition_term("Lackierung", response))
                l.add_value('cylinders', self.parse_definition_term("Zylinder", response))
                l.add_value('upholstery', self.parse_upholstery(response))
                l.add_value('fuel_types', self.parse_fuel_types(response))
                l.add_value('price_label_ranges', self.parse_price_label_ranges(response))
                l.add_value('next_inspection', self.parse_next_inspection(response))
                l.add_value('emissions', self.parse_emissions(response))
                l.add_value('consumption', self.parse_consumption(response))
                l.add_value('adress', self.parse_adress(response))
                l.add_value('crawled', datetime.now().isoformat())
                l.add_value('url', response.url)
                yield l.load_item()
            else: self.logger.warn(f'{response.url} was {response.status} but did not contain [.cldt-item[data-item-name="car-details"]')
        except:
            self.logger.error(traceback.format_exc())

    def parse_adress(self, response):
        a = ItemLoader(item=AdressItem(), selector=response)
        a.add_css('city', '[data-item-name=vendor-contact-city]::text')
        a.add_css('area_code', "[as24-tracking-value*='classified_zipcode']::attr('as24-tracking-value')")
        a.add_css('country', "[as24-tracking-value*='classified_country']::attr('as24-tracking-value')")
        return a.load_item()

    def parse_emissions(self, response):
        e = ItemLoader(item=EmissionItem(), selector=response)
        e.add_css('co2', "[as24-tracking-value*='classified_emission\":']::attr('as24-tracking-value')")
        e.add_css('standard', "[as24-tracking-value*='classified_emissionStandard']::attr('as24-tracking-value')")
        e.add_value('label', self.parse_definition_term("Feinstaubplakette", response))
        return e.load_item()

    def parse_consumption(self, response):
        c = ItemLoader(item=ConsumptionItem(), selector=response)
        c.add_css('combined', "[as24-tracking-value*='classified_consumption']::attr('as24-tracking-value')")
        c.add_value('electric', self.parse_electric_consumption(response))
        return c.load_item()

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

    def parse_exists_node_with_inner_html(self, response, inner_html):
        node = response.xpath(f'//dt[. = "{inner_html}"]')
        return True if node else None

    def parse_next_inspection(self, response):
        next_inspection = self.parse_definition_term("HU Prüfung", response)
        if (next_inspection): return datetime.strptime(next_inspection, '%M/%Y').isoformat()

    def parse_electric_consumption(self, response):
        electric_consumption = response.xpath('//dt[contains(text(), "Stromverbrauch")]')
        if electric_consumption:
            dt = response.xpath('//dt[contains(text(), "Stromverbrauch")]/following-sibling::dd[1]/text()').extract_first().split('kWh')
            return float(dt[0].strip().replace(',', '.'))

    def parse_fuel_types(self, response):
        fuel_types = self.parse_definition_term("Kraftstoff", response)
        if (fuel_types): return fuel_types.split("/")

    def parse_upholstery(self, response):
        upholstery = self.parse_definition_term("Innenausstattung", response)
        if (upholstery): return upholstery.split(',')

    def parse_definition_term(self, term: str, response: TextResponse):
        dt = response.xpath(f'//dt[. = "{term}"]')
        if (dt is None): return None
        dd = response.xpath(f'//dt[. = "{term}"]/following-sibling::dd[1]/a/text()').extract_first()
        if (dd is not None): return dd.strip()
        dd = response.xpath(f'//dt[. = "{term}"]/following-sibling::dd[1]/text()').extract_first()
        if (dd is not None): return dd.strip()
        return None