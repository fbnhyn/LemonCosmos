from datetime import datetime
from logging import NOTSET
from lmpd.lemon.lemon.spiders.lemon_spider import LemonSpider

from twisted.internet import defer, reactor
from lmpd.cosmos.service import CosmosService
from scrapy.crawler import CrawlerRunner

def run():
    service = CosmosService()
    makers = list(service.get_all_makers())

    runner = CrawlerRunner()
    query_jobs = []

    # m = service.get_maker_by_id("27")
    # for maker in [m]:
    
    for maker in makers:
        makerQuery = maker.get('query')
        if (makerQuery is None): continue
        if (makerQuery.get('urls') is None): continue
        if (makerQuery.get('crawled')): continue
        if (makerQuery.get('hits') == 0): continue
        query_jobs.append({
            'maker_id': maker.get('id'),
            'maker': maker.get('name'),
            'start_urls': makerQuery.get('urls')
        })
    
    crawl(query_jobs, runner, service)
    reactor.run()

@defer.inlineCallbacks
def crawl(query_job, runner: CrawlerRunner, service: CosmosService):
    for job in query_job:
        print(f'### {job.get("maker")} ###')
        yield runner.crawl(LemonSpider, start_urls=job.get('start_urls'))
        print(f'--- {job.get("maker")} ---')
    reactor.stop()

if __name__ == '__main__': run()