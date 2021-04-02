from datetime import datetime
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

    crawl(query_jobs, runner, service)
    reactor.run()

@defer.inlineCallbacks
def crawl(query_jobs, runner: CrawlerRunner, service: CosmosService):
    for job in query_jobs:
        print(f'### {job.get("maker")} ###')
        QuerySpider.result.hits = 0
        QuerySpider.result.urls = []
        QuerySpider.result.time = datetime.now().isoformat()
        yield runner.crawl(QuerySpider, start_urls=job.get('start_urls'))
        service.update_maker_query(job.get('maker_id'), QuerySpider.result)
        print(f'--- {job.get("maker")}: {QuerySpider.result.hits} ---')
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