from datetime import datetime
import json
import os
from azure.cosmos import CosmosClient, PartitionKey
from azure.cosmos.container import ContainerProxy
from dotenv import load_dotenv

class CosmosService:

    def __init__(self):
        load_dotenv()
        _endpoint = os.getenv('ENDPOINT')
        _key = os.getenv('KEY')
        _db_name = os.getenv('DATABASE_NAME')
        _lemons_container_name = os.getenv('CONTAINER_LEMONS_NAME')
        _makers_models_container_name = os.getenv('CONTAINER_MAKERS_NAME')

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

    def insert_lemon(self, json):
        self.lemons_container.create_item(json)

    def insert_maker(self, json):
        self.makers_models_container.create_item(json)

    def upsert_maker(self, maker):
        try:
            self.makers_models_container.upsert_item(body=maker)
        except:
            print(f'error while upserting maker {maker.get("makerId")}')

    def get_maker_by_id(self, makerId):
        makers = list(self.makers_models_container.query_items(
            query= f'SELECT TOP 1 m FROM makers m WHERE m.id = "{makerId}"',
            enable_cross_partition_query=True))
        return makers[0].get('m')

    def append_query_urls_to_maker(self, makerId, query_urls):
        maker = self.get_maker_by_id(makerId)
        if maker.get('query_urls') is None:
            maker['query_urls'] = []
        maker['query_urls'].append({
            datetime.now().isoformat(): query_urls
        })
        self.upsert_maker(maker)

    def get_all_maker_names(self):
        for m in self.makers_models_container.query_items(
                query='SELECT m.name FROM makers m',
                enable_cross_partition_query=True):
            yield m