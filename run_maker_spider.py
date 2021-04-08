import logging
from scrapy.crawler import CrawlerProcess
from lmpd.lemon.lemon.spiders.maker_spider import MakerSpider

def run():
    logging.basicConfig(
        filename='Logs/maker.log',
        level=logging.ERROR,
        format='%(asctime)s %(name)-12s %(levelname)-12s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        filemode='a')

    logger = logging.getLogger('RunMakerSpider')
    logger.setLevel(logging.INFO)

    process = CrawlerProcess()
    process.crawl(MakerSpider)
    process.start()

if __name__ == '__main__': run()