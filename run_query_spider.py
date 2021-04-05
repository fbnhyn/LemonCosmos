from datetime import datetime
import logging
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
        filename='Logs\\query.log',
        level=logging.ERROR,
        format='%(asctime)s %(levelname)-8s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        filemode='w')

    logger = logging.getLogger('RunQuerySpider')
    logger.setLevel(logging.INFO)

    service = CosmosService()
    makers = list(service.get_all_makers())

    runner = CrawlerRunner()
    query_jobs = []

    for maker in makers:
        query_jobs.append({
            'maker_id': maker.get('id'),
            'maker': maker.get('name'),
            'start_urls': build_start_urls(maker)
        })

    crawl(query_jobs, logger, runner, service)
    reactor.run()

@defer.inlineCallbacks
def crawl(query_jobs, logger: logging.Logger, runner: CrawlerRunner, service: CosmosService):
    for job in query_jobs:
        logger.info(f'Start getting queries for {job.get("maker")}')
        QuerySpider.result.hits = 0
        QuerySpider.result.urls = []
        QuerySpider.result.time = datetime.now().isoformat()
        yield runner.crawl(QuerySpider, start_urls=job.get('start_urls'))
        service.update_maker_query(job.get('maker_id'), QuerySpider.result)
    reactor.stop()

def build_start_urls(maker):
    urls = []
    for m in maker.get('models'):
        if maker.get('is_top'):
            for c in countries:
                urls.append(f'https://www.autoscout24.de/lst/{quote(maker.get("name"))}/{quote(m.get("name"))}?size=20&offer={",".join(offer_types)}&cy={c}')
        else:
            urls.append(f'https://www.autoscout24.de/lst/{quote(maker.get("name"))}/{quote(m.get("name"))}?size=20&offer={",".join(offer_types)}')
    return urls

if __name__ == '__main__': run()