from scrapy import settings
from scrapy.crawler import CrawlerProcess, CrawlerRunner
from lmpd.cosmos.service import CosmosService
from lmpd.lemon.lemon.spiders.maker_spider import MakerSpider

process = CrawlerProcess()
process.crawl(MakerSpider)
process.start()