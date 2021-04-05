import logging

from twisted.internet import defer, reactor
from scrapy.crawler import CrawlerRunner
from lmpd.lemon.lemon.spiders.lemon_spider import LemonSpider
from lmpd.cosmos.service import CosmosService


def run():
    logging.basicConfig(
        filename='Logs\\lemons.log',
        level=logging.ERROR,
        format='%(asctime)s %(levelname)-8s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        filemode='w')

    logger = logging.getLogger('RunLemonSpider')
    logger.setLevel(logging.INFO)

    service = CosmosService()
    runner = CrawlerRunner()

    makers = service.get_makers_to_crawl()
    query_jobs = []

    for m in makers:
        maker = service.get_urls_by_maker(m.get('id'))
        makerQuery = maker.get('query')
        query_jobs.append({
            'maker_id': maker.get('id'),
            'maker': maker.get('name'),
            'start_urls': makerQuery.get('urls')
        })
    
    crawl(query_jobs, logger, runner, service)
    reactor.run()

@defer.inlineCallbacks
def crawl(query_job, logger:logging.Logger, runner: CrawlerRunner, service: CosmosService):
    for job in query_job:
        logger.info(f'Starting crawling for {job.get("maker")}')
        yield runner.crawl(LemonSpider, start_urls=job.get('start_urls'))
        service.mark_as_crawled(job.get('maker_id'))
    reactor.stop()

if __name__ == '__main__': run()