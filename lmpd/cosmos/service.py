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
        _makers_container_name = os.getenv('CONTAINER_MAKERS_NAME')
        _models_container_name = os.getenv('CONTAINER_MODELS_NAME')
        _lemons_pk = os.getenv('CONTAINER_LEMONS_PARTITIONKEY')
        _makers_pk = os.getenv('CONTAINER_MAKERS_PARTITIONKEY')
        _models_pk = os.getenv('CONTAINER_MODELS_PARTITIONKEY')

        client = CosmosClient(_endpoint, _key)
        db = client.create_database_if_not_exists(id=_db_name)

        self.lemons_container = db.create_container_if_not_exists(
            id=_lemons_container_name, partition_key=PartitionKey(path=_lemons_pk)
        )

        self.makers_container = db.create_container_if_not_exists(
            id=_makers_container_name, partition_key=PartitionKey(path=_makers_pk)
        )

        self.models_container = db.create_container_if_not_exists(
            id=_models_container_name, partition_key=PartitionKey(path=_models_pk)
        )

    def insert_lemon(self, json):
        self.lemons_container.create_item(json)

    def insert_maker(self, json):
        self.makers_container.create_item(json)

    def insert_model(self, json):
        self.models_container.create_item(json)
