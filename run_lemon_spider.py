from datetime import datetime
from logging import NOTSET
from lmpd.lemon.lemon.spiders.lemon_spider import LemonSpider

from twisted.internet import defer, reactor
from lmpd.cosmos.service import CosmosService
from scrapy.crawler import CrawlerRunner

def run():
    service = CosmosService()
    maker_ids = list(service.get_makers_to_crawl())

    runner = CrawlerRunner()
    query_jobs = []

    # m = service.get_maker_by_id("27")
    # for maker in [m]:

    for maker_id in maker_ids:
        maker = service.get_urls_by_maker(maker_id)
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