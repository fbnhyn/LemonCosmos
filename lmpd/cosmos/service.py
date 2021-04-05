import logging
import traceback
import os

from azure.cosmos.exceptions import CosmosResourceExistsError
from lmpd.lemon.lemon.models import QueryResult
from azure.cosmos import CosmosClient, PartitionKey
from dotenv import load_dotenv

class CosmosService:

    def __init__(self):
        load_dotenv()
        _endpoint = os.getenv('ENDPOINT')
        _key = os.getenv('KEY')
        _db_name = os.getenv('DATABASE_NAME')
        _lemons_container_name = os.getenv('CONTAINER_LEMONS_NAME')
        _makers_models_container_name = os.getenv('CONTAINER_MAKERS_NAME')

        self.logger = logging.getLogger('CosmosService')
        self.logger.setLevel(logging.ERROR)

        self.lemons_pk = os.getenv('CONTAINER_LEMONS_PARTITIONKEY')
        self.makers_models_pk = os.getenv('CONTAINER_MAKERS_PARTITIONKEY')

        client = CosmosClient(_endpoint, _key)
        db = client.create_database_if_not_exists(id=_db_name)

        self.lemons_container = db.create_container_if_not_exists(
            id=_lemons_container_name, partition_key=PartitionKey(path=self.lemons_pk)
        )

        self.makers_models_container = db.create_container_if_not_exists(
            id=_makers_models_container_name, partition_key=PartitionKey(path=self.makers_models_pk)
        )

    def upsert_lemon(self, lemon):
        try:
            self.lemons_container.upsert_item(body=lemon)
            self.logger.info(f'Upserted {lemon.get("make_name")}\t{lemon.get("model_name")}\t{lemon.get("id")}')
        except:
            self.logger.error(traceback.format_exc())

    def insert_maker(self, maker):
        try:
            self.makers_models_container.create_item(maker)
            self.logger.info(f'''Added new maker
            {maker}''')
        except CosmosResourceExistsError:
            self.logger.info(f'Maker {maker["name"]} already exists')
        except: 
            self.logger.error(traceback.format_exc())

    def upsert_maker(self, maker):
        try:
            self.makers_models_container.upsert_item(body=maker)
            self.logger.info(f'''Added new models for {maker["name"]}
            {maker["models"]}''')
        except:
            self.logger.error(traceback.format_exc())

    def get_maker_by_id(self, makerId):
        maker = list(self.makers_models_container.query_items(
            query= f'SELECT * FROM m WHERE m.id = "{makerId}"',
            enable_cross_partition_query=True))
        return maker[0]

    def update_maker_query(self, makerId, query_result: QueryResult):
        maker = self.get_maker_by_id(makerId)
        maker["query"] = {
            'crawled': False,
            'hits': query_result.hits,
            'time': query_result.time,
            'urls': query_result.urls
        }
        self.upsert_maker(maker)

    def mark_as_crawled(self, makerid):
        maker = self.get_maker_by_id(makerid)
        maker['query']['crawled'] = True
        self.upsert_maker(maker)
        self.logger.info(f'Marked {maker.get("name")} as crawled')

    def get_all_maker_names(self):
        for m in self.makers_models_container.query_items(
                query='SELECT m.name FROM makers m',
                enable_cross_partition_query=True):
            yield m

    def get_all_makers(self):
        for m in self.makers_models_container.query_items(
                query='SELECT * FROM makers m',
                enable_cross_partition_query=True):
            yield m

    def get_makers_to_crawl(self):
        for m in self.makers_models_container.query_items(
                query='''
                SELECT m.id FROM makers m
                WHERE m.query.crawled = false AND m.query.hits > 0
                ORDER BY m.query.time''',
                enable_cross_partition_query=True):
            yield m

    def get_urls_by_maker(self, maker_id):
        makers = list(self.makers_models_container.query_items(
            query=f'''
            SELECT m.id, m.name, m.query FROM makers m
            WHERE m.id = "{maker_id}"''',
            enable_cross_partition_query=True))
        return makers[0]