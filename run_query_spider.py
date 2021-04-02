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

@defer.inlineCallbacks
def crawl(limen_spider_jobs):
    for job in limen_spider_jobs:
        print(f'### {job.get("maker")} ###')
        QuerySpider.result.hits = 0
        QuerySpider.result.urls = []
        QuerySpider.result.time = datetime.now().isoformat()
        yield runner.crawl(QuerySpider, start_urls=job.get('query_urls'))
        # service.append_query_result_to_maker(job.get('maker_id'), QuerySpider.result)
        print(f'--- {job.get("maker")}: {QuerySpider.result.hits} ---')
    reactor.stop()

def build_start_urls(maker):
    urls = []
    for m in maker.get('models'):
        # if query_by_county:
        if maker.get('is_top'):
            for c in countries:
                urls.append(f'https://www.autoscout24.de/lst/{quote(maker.get("name"))}/{quote(m.get("name"))}?size=20&offer={",".join(offer_types)}&cy={c}')
        else:
            urls.append(f'https://www.autoscout24.de/lst/{quote(maker.get("name"))}/{quote(m.get("name"))}?size=20&offer={",".join(offer_types)}')
    return urls

service = CosmosService()
makers = list(service.get_all_makers())

runner = CrawlerRunner()
lemon_spider_jobs = []

m = service.get_maker_by_id("74")

for maker in [m]:
    lemon_spider_jobs.append({
        'maker_id': maker.get('id'),
        'maker': maker.get('name'),
        'query_urls': build_start_urls(m)
    })

crawl(lemon_spider_jobs)
reactor.run()