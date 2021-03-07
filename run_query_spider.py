from datetime import datetime
from lmpd.lemon.lemon.spiders.query_spider import QuerySpider
from urllib.parse import quote

from twisted.internet import defer, reactor
from lmpd.cosmos.service import CosmosService
from scrapy.crawler import CrawlerRunner

@defer.inlineCallbacks
def crawl(limen_spider_jobs):
    for job in limen_spider_jobs:
        print(f'start crawling queries for {job.get("maker")}')
        QuerySpider.result.hits = 0
        QuerySpider.result.urls = []
        QuerySpider.result.time = datetime.now().isoformat()
        yield runner.crawl(QuerySpider, start_urls=job.get('query_urls'))
        service.append_query_result_to_maker(job.get('maker_id'), QuerySpider.result)
        print(f'crawled queries for {job.get("maker")}')
    reactor.stop()

service = CosmosService()
makers = list(service.get_all_makers())

runner = CrawlerRunner()
lemon_spider_jobs = []

for maker in makers:
    query_urls = []

    for m in maker.get('models'):

        for c in ['A', 'B', 'D', 'E', 'F', 'I', 'L', 'NL']:
            query_urls.append(f'https://www.autoscout24.de/lst/{quote(maker.get("name"))}/{quote(m.get("name"))}?size=20&offer=U,u&cy={c}')

    lemon_spider_jobs.append({
        'maker_id': maker.get('id'),
        'maker': maker.get('name'),
        'query_urls': query_urls
    })

crawl(lemon_spider_jobs)
reactor.run()