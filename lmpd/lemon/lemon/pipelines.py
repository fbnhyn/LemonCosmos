# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from itemadapter import ItemAdapter
from lmpd.cosmos.service import CosmosService

class CosmosPipeline():
    service = CosmosService()

class LemonPipeline(CosmosPipeline):

    def process_item(self, item, spider):
        self.service.insert_lemon(ItemAdapter(item).asdict())

class MakersPipeline(CosmosPipeline):

    def process_item(self, item, spider):
        self.service.insert_maker(ItemAdapter(item).asdict())