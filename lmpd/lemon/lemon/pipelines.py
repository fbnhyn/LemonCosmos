# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import logging
import sys
from typing import Dict
from itemadapter import ItemAdapter
from lmpd.cosmos.service import CosmosService
from azure.cosmos.exceptions import CosmosResourceExistsError

class CosmosPipeline():
    service = CosmosService()
    logger = logging.getLogger('CosmosPipeline')

class LemonPipeline(CosmosPipeline):

    def process_item(self, item, spider):
        self.service.upsert_lemon(ItemAdapter(item).asdict())

class MakersPipeline(CosmosPipeline):

    def process_item(self, item, spider):
        self.service.insert_maker(ItemAdapter(item).asdict())

class ModelsPipeline(CosmosPipeline):

    def process_item(self, maker: Dict, spider):
        update_maker = False
        maker = self.service.get_maker_by_id(maker.get('maker_id'))
        maker_models = maker.get('models')
        scraped_models = maker.get('models')

        if maker_models is None:
            maker_models = []

        for model in scraped_models:
            if not any(m.get('id') == model.get('id') for m in maker_models):
                self.logger.info(f'Added new model {model: <12} for {maker.get("name")}')
                maker_models.append(model)
                update_maker = True

        if update_maker:
            maker['models'] = maker_models
            self.service.upsert_maker(maker)
        else:
            self.logger.info(f'No new models for {maker.get("name")}')
