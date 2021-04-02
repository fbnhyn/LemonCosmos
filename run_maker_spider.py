from scrapy.crawler import CrawlerProcess
from lmpd.lemon.lemon.spiders.maker_spider import MakerSpider

def run():
    process = CrawlerProcess()
    process.crawl(MakerSpider)
    process.start()

if __name__ == '__main__': run()