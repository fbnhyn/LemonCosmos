from datetime import datetime
from logging import NOTSET
from lmpd.lemon.lemon.spiders.lemon_spider import LemonSpider

from twisted.internet import defer, reactor
from lmpd.cosmos.service import CosmosService
from scrapy.crawler import CrawlerRunner

def run():
    service = CosmosService()
    makers = list(service.get_makers_to_crawl())

    runner = CrawlerRunner()
    query_jobs = []

    for m in makers:
        maker = service.get_urls_by_maker(m.get('id'))
        makerQuery = maker.get('query')
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
        service.mark_as_crawled(job.get('maker_id'))
        print(f'--- {job.get("maker")} ---')
    reactor.stop()

if __name__ == '__main__': run()