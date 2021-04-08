import logging
from scrapy.crawler import CrawlerProcess
from lmpd.lemon.lemon.spiders.maker_spider import MakerSpider

def run():

    logging.basicConfig(
        filename='Logs/makers.log',
        level=logging.ERROR,
        format='%(asctime)s %(name)-16s %(levelname)-16s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        filemode='w')

    logging.getLogger("azure").setLevel(logging.ERROR)
    logging.getLogger("urllib3").setLevel(logging.ERROR)

    logger = logging.getLogger('RunMakerSpider')
    logger.setLevel(logging.INFO)

    process = CrawlerProcess()
    process.crawl(MakerSpider)
    process.start()

if __name__ == '__main__': run()