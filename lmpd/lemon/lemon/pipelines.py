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

class ModelsPipeline(CosmosPipeline):

    def process_item(self, item, spider):
        update_maker = False
        maker = self.service.get_maker_by_id(item.get('makerId'))
        maker_models = maker.get('models')
        scraped_models = item.get('models')

        for sm in scraped_models:
            if not any(m['id'] == sm.get('id') for m in maker_models):
                maker_models.append(sm)
                update_maker = True

        if update_maker:
            maker['models'] = maker_models
            self.service.insert_maker_embedded_models(maker)
            print(f"Scraped new models for maker {item.get('makerId')}")
        else:
            print(f"No new models for maker {item.get('makerId')}")
