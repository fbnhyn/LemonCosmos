from scrapy.crawler import CrawlerProcess
from lmpd.lemon.lemon.spiders.maker_spider import MakerSpider

process = CrawlerProcess()
process.crawl(MakerSpider)
process.start()