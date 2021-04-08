import logging
import traceback

from twisted.internet import defer, reactor
from scrapy.crawler import CrawlerRunner
from lmpd.lemon.lemon.spiders.lemon_spider import LemonSpider
from lmpd.cosmos.service import CosmosService

def run():
    logging.basicConfig(
        filename='Logs/lemons.log',
        level=logging.ERROR,
        format='%(asctime)s %(name)-12s %(levelname)-12s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        filemode='w')

    logger = logging.getLogger('RunLemonSpider')
    logger.setLevel(logging.INFO)

    service = CosmosService()
    runner = CrawlerRunner()

    makers = service.get_maker_by_id("51539")

    for maker in [makers]:
        crawl(maker, logger, runner, service)
        reactor.run()


@defer.inlineCallbacks
def crawl(maker, logger:logging.Logger, runner: CrawlerRunner, service: CosmosService):
    try:
        maker = service.get_urls_by_maker(maker.get('id'))
        logger.info(f'Starting crawling for {maker.get("name")}')
        yield runner.crawl(LemonSpider, start_urls=maker['query']['urls'])
        service.mark_as_crawled(maker.get('name'))
        reactor.stop()
    except:
        logger.error(traceback.format_exc())

if __name__ == '__main__': run()