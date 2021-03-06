# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from attr import set_run_validators
import scrapy
import json
import re
from datetime import datetime
from itemloaders.processors import TakeFirst, MapCompose
import w3lib.html as w3

def return_int(value: str):
    if (value):
        return int(value)

def return_float(value: str):
    return float(value)

def return_bool(value: str):
    return True if value == 'true' else False

def return_dict_value(value: str):
    _d = json.loads(value)
    return _d.values()

def return_only_letters(value: str):
    return re.sub(r'\d+\s', '', value).strip()

def return_only_digits(value: str): 
    return re.sub(r'\D', '',  value)

def return_list_from_string(value: str):
    return value.split(',')

def string_before_dash(value: str):
    return value.split()[0]

def string_after_dash(value: str):
    return value.split()[-1]


class EquipmentItem(scrapy.Item): 
    id = scrapy.Field(
        input_processor=MapCompose(w3.remove_tags, return_only_digits, return_int),
        output_processor=TakeFirst()
    ) 
    name = scrapy.Field(
        input_processor=MapCompose(w3.remove_tags),
        output_processor=TakeFirst()
    )

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
    city = scrapy.Field(
        input_processor=MapCompose(return_only_letters),
        output_processor=TakeFirst()
    )
    area_code = scrapy.Field(
        input_processor=MapCompose(return_dict_value),
        output_processor=TakeFirst()
    )
    country = scrapy.Field(
        input_processor=MapCompose(return_dict_value),
        output_processor=TakeFirst()
    )

class PriceRangeItem(scrapy.Item):
    start = scrapy.Field(
        input_processor=MapCompose(w3.remove_tags, string_before_dash, return_only_digits, return_int),
        output_processor=TakeFirst()
    )
    end = scrapy.Field(
        input_processor=MapCompose(w3.remove_tags, string_after_dash, return_only_digits, return_int),
        output_processor=TakeFirst()
    )

class PriceLabelRangesItem(scrapy.Item):
    top = scrapy.Field(
        serializer=PriceRangeItem,
        output_processor=TakeFirst()
    )
    good = scrapy.Field(
        serializer=PriceRangeItem,
        output_processor=TakeFirst()
    )
    fair = scrapy.Field(
        serializer=PriceRangeItem,
        output_processor=TakeFirst()
    )
    somewhat = scrapy.Field(
        serializer=PriceRangeItem,
        output_processor=TakeFirst()
    )
    expensiv = scrapy.Field(
        serializer=PriceRangeItem,
        output_processor=TakeFirst()
    )

class EmissionItem(scrapy.Item):
    eclass = scrapy.Field()
    label = scrapy.Field()
    co2 = scrapy.Field(
        input_processor=MapCompose(return_dict_value, return_float),
        output_processor=TakeFirst()
    )
    standard = scrapy.Field(
        input_processor=MapCompose(return_dict_value, return_int),
        output_processor=TakeFirst()
    )

class ConsumptionItem(scrapy.Item):
    combined: scrapy.Field()
    city: scrapy.Field()
    country: scrapy.Field()

class LemonItem(scrapy.Item):
    # Meta
    id = scrapy.Field(
        input_processor=MapCompose(return_dict_value),
        output_processor=TakeFirst()
    )
    origin = scrapy.Field(
        input_processor=MapCompose(return_dict_value),
        output_processor=TakeFirst()
    )
    crawled = scrapy.Field(
        output_processor=TakeFirst()
    )
    is_superdeal =  scrapy.Field(
        input_processor=MapCompose(return_dict_value, return_bool),
        output_processor=TakeFirst()
    )

    # Pricinginformation
    price = scrapy.Field(
        input_processor=MapCompose(return_dict_value, return_int),
        output_processor=TakeFirst()
    )
    price_label = scrapy.Field(
        input_processor=MapCompose(return_dict_value),
        output_processor=TakeFirst()
    )
    price_label_ranges = scrapy.Field(
        serializer=PriceLabelRangesItem,
        output_processor=TakeFirst()
    )

    # Overview
    description = scrapy.Field(),
    milage = scrapy.Field(
        input_processor=MapCompose(return_dict_value, return_int),
        output_processor=TakeFirst()
    )
    offer_type = scrapy.Field(
        input_processor=MapCompose(return_dict_value),
        output_processor=TakeFirst()
    )
    first_registration = scrapy.Field()
    year = scrapy.Field(
        input_processor=MapCompose(return_dict_value),
        output_processor=TakeFirst()
    )
    pre_owners = scrapy.Field()
    power = scrapy.Field(
        input_processor=MapCompose(return_dict_value, return_int),
        output_processor=TakeFirst()
    )
    engine_type = scrapy.Field()
    fuel_type = scrapy.Field(
        input_processor=MapCompose(return_dict_value),
        output_processor=TakeFirst()
    )
    highlights = scrapy.Field()

    # Properties
    makeId = scrapy.Field(
        input_processor=MapCompose(return_dict_value),
        output_processor=TakeFirst()
    )
    makeName =scrapy.Field(
        input_processor=MapCompose(return_dict_value),
        output_processor=TakeFirst()
    )
    modelId = scrapy.Field(
        input_processor=MapCompose(return_dict_value),
        output_processor=TakeFirst()
    )
    modelName = scrapy.Field(
        input_processor=MapCompose(return_dict_value),
        output_processor=TakeFirst()
    )
    segment = scrapy.Field(
        input_processor=MapCompose(return_dict_value),
        output_processor=TakeFirst()
    )
    color = scrapy.Field()
    paint_type = scrapy.Field()
    upholstery = scrapy.Field() # array
    body = scrapy.Field() # array
    doors = scrapy.Field(
        input_processor=MapCompose(return_dict_value, return_int),
        output_processor=TakeFirst()
    )
    seats = scrapy.Field(
        input_processor=MapCompose(return_dict_value, return_int),
        output_processor=TakeFirst()
    )
    country_version = scrapy.Field()
    equipment_codes = scrapy.Field(
        input_processor=MapCompose(return_dict_value, return_list_from_string)
    )
    # Zustand
    origin = scrapy.Field(
        input_processor=MapCompose(return_dict_value),
        output_processor=TakeFirst()
    )
    # Hubraum
    capacity = scrapy.Field(
        input_processor=MapCompose(return_dict_value, return_int),
        output_processor=TakeFirst()
    )

    # State
    state_type = scrapy.Field() # condition of the lemon
    hu_check = scrapy.Field()
    smoke_free = scrapy.Field()
    warranty = scrapy.Field()
    full_service = scrapy.Field()
    new_inspection = scrapy.Field()

    # Drive
    fuels = scrapy.Field() # array
    consumption = scrapy.Field(
        input_processor=MapCompose(return_dict_value, return_float),
        output_processor=TakeFirst()
    )
    drive_chain = scrapy.Field()
    gears = scrapy.Field()
    displacement = scrapy.Field()
    cylinders = scrapy.Field()
    weight = scrapy.Field()
    emissions = scrapy.Field(
        serializer=EmissionItem,
        output_processor=TakeFirst()
    )

    # Regional Information
    adress =  scrapy.Field(
        serializer=AdressItem,
        output_processor=TakeFirst()
    )

    # Equipment
    equipment = scrapy.Field(
        input_processor=MapCompose(w3.remove_tags)
    )

    # Autoscout24 Ad Targeting
    ad_targeting = scrapy.Field() # response.css("s24-ad-targeting")[1] // save as json