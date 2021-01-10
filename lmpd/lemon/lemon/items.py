# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from datetime import datetime
from dataclasses import dataclass
from itemloaders.processors import TakeFirst, MapCompose
import w3lib.html as w3

def return_int(value):
    return int(value)

def return_bool(value):
    return True if value == 'true' else False

class ModelItem(scrapy.Item):
    id = scrapy.Field(
        input_processor=MapCompose(w3.remove_tags),
        output_processor=TakeFirst()
    ) 
    name = scrapy.Field(
        input_processor=MapCompose(w3.remove_tags),
        output_processor=TakeFirst()
    )

class MakerItem(scrapy.Item):
    id = scrapy.Field(
        input_processor=MapCompose(w3.remove_tags),
        output_processor=TakeFirst()
    ) 
    name = scrapy.Field(
        input_processor=MapCompose(w3.remove_tags),
        output_processor=TakeFirst()
    )
    isTop = scrapy.Field(
        input_processor=MapCompose(w3.remove_tags, return_bool),
        output_processor=TakeFirst()
    )

class AdressItem(scrapy.Item):
    area_code = scrapy.Field()
    city = scrapy.Field()
    # FIX: country can be extracted via response // request url; Get char(s) after cy= and before &
    country = scrapy.Field()

class PriceRange(scrapy.Item):
    start = scrapy.Field()
    end = scrapy.Field()

class PriceLabelRangesItem(scrapy.Item):
    top = PriceRange()
    good = PriceRange()
    fair = PriceRange()
    somewhat = PriceRange()
    expensiv = PriceRange()

class EmissionItem(scrapy.Item):
    co2 = scrapy.Field()
    eclass = scrapy.Field()
    label = scrapy.Field()

class ConsumptionItem(scrapy.Item):
    combined: scrapy.Field()
    city: scrapy.Field()
    country: scrapy.Field()

class LemonItem(scrapy.Item):
    # Meta
    id = scrapy.Field()
    crawled = datetime.now()

    # Pricinginformation
    price = scrapy.Field()
    price_label = scrapy.Field()
    price_label_ranges = PriceLabelRangesItem()

    # Overview
    description = scrapy.Field()
    milage = scrapy.Field()
    offer_type = scrapy.Field() # dealer or privat offer
    first_registration = scrapy.Field()
    pre_owners = scrapy.Field()
    power = scrapy.Field()
    engine_type = scrapy.Field()
    fuel_type = scrapy.Field()
    highlights = scrapy.Field()

    # Properties
    make = scrapy.Field()
    model = scrapy.Field()
    color = scrapy.Field()
    paint_type = scrapy.Field()
    upholstery = scrapy.Field() # array
    body = scrapy.Field() # array
    doors = scrapy.Field()
    seats = scrapy.Field()
    model_code = scrapy.Field()
    country_version = scrapy.Field()

    # State
    state_type = scrapy.Field() # condition of the lemon
    hu_check = scrapy.Field()
    smoke_free = scrapy.Field()
    warranty = scrapy.Field()
    full_service = scrapy.Field()
    new_inspection = scrapy.Field()

    # Drive
    fuels = scrapy.Field() # array
    consumption = scrapy.Field()
    drive_chain = scrapy.Field()
    gears = scrapy.Field()
    displacement = scrapy.Field()
    cylinders = scrapy.Field()
    weight = scrapy.Field()
    emission = EmissionItem()

    # Regional Information
    adress = AdressItem()

    # Equipment
    comfort = scrapy.Field() # array
    entertainment = scrapy.Field() # array
    safety = scrapy.Field() # array
    extras = scrapy.Field() # array

    # Autoscout24 Ad Targeting
    ad_targeting = scrapy.Field() # response.css("s24-ad-targeting")[1] // save as json
    classified_flields= scrapy.Field() # response.css(as42-tracking[type=gtm][action=set]:not([as24-tracking-click-target]))
