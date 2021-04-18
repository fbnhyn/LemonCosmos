import logging
from datetime import datetime
import sys
from lmpd.lemon.lemon.spiders.query_spider import QuerySpider
from urllib.parse import quote

from twisted.internet import defer, reactor
from lmpd.cosmos.service import CosmosService
from scrapy.crawler import CrawlerRunner

offer_types = [
    'D', # Demo
    'J', # Jahreswagen
    'O', # Oldtimer
    'U'  # Gebraucht
]

query_by_county = False

countries = [
    'A', # Österreich
    'B', # Belgien
    'D', # Deutschland
    'E', # Spanien
    'F', # Frankreich
    'I', # Italien
    'L', # Luxemburg
    'NL' # Niederlande
]

def run():
    logging.basicConfig(
        filename='Logs/query.log',
        level=logging.ERROR,
        format='%(asctime)s %(name)-12s %(levelname)-12s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        filemode='w')

    logger = logging.getLogger("RunQuerySpider")
    logger.setLevel(logging.INFO)

    service = CosmosService()
    makers = service.get_all_makers()

    runner = CrawlerRunner()

    for maker in makers:
        crawl(maker, logger, runner, service)
        reactor.run()

@defer.inlineCallbacks
def crawl(maker, logger: logging.Logger, runner: CrawlerRunner, service: CosmosService):
    maker = service.get_maker_by_id(maker.get("id"))
    logger.info(f'Start getting queries for {maker.get("name")}')
    QuerySpider.result.hits = 0
    QuerySpider.result.urls = []
    QuerySpider.result.time = datetime.now().isoformat()
    yield runner.crawl(QuerySpider, start_urls=build_start_urls(maker))
    service.update_maker_query(maker.get("id"), QuerySpider.result)
    reactor.stop()

def build_start_urls(maker):
    urls = []
    for m in maker.get('models'):
        if maker.get('is_top'):
            for c in countries:
                urls.append(f'https://www.autoscout24.de/lst/{quote(maker.get("name"))}/{quote(m.get("name"))}?sort=age&size=20&offer={",".join(offer_types)}&cy={c}')
        else:
            urls.append(f'https://www.autoscout24.de/lst/{quote(maker.get("name"))}/{quote(m.get("name"))}?sort=age&size=20&offer={",".join(offer_types)}')
    return urls

if __name__ == '__main__': run()