from scrapy.crawler import CrawlerProcess
from lmpd.lemon.lemon.spiders.model_spider import ModelSpider
from lmpd.cosmos.service import CosmosService

cs= CosmosService()
makers = cs.get_all_makers()
start_urls = []
for m in makers:
    start_urls.append(f'http://autoscout24.de/lst/{m.get("name")}')

process = CrawlerProcess()
process.crawl(ModelSpider, start_urls=start_urls)
process.start()