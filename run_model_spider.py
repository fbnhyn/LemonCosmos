import logging
import sys
from scrapy.crawler import CrawlerProcess
from lmpd.lemon.lemon.spiders.model_spider import ModelSpider
from lmpd.cosmos.service import CosmosService

def run():
    logging.basicConfig(
        filename='Logs/models.log',
        level=logging.ERROR,
        format='%(asctime)s %(name)-12s %(levelname)-12s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        filemode='a')

    logger = logging.getLogger('RunModelSpider')
    logger.setLevel(logging.ERROR)

    service = CosmosService()
    makers = service.get_all_maker_names()
    start_urls = []
    for m in makers:
        start_urls.append(f'http://autoscout24.de/lst/{m.get("name")}')

    process = CrawlerProcess()
    process.crawl(ModelSpider, start_urls=start_urls)
    process.start()

if __name__ == '__main__': run()