from lmpd.lemon.lemon.spiders.query_spider import QuerySpider
from urllib.parse import quote

from twisted.internet import defer, reactor
from lmpd.cosmos.service import CosmosService
from scrapy.crawler import CrawlerRunner

@defer.inlineCallbacks
def crawl(limen_spider_jobs):
    for job in limen_spider_jobs:
        yield runner.crawl(QuerySpider, start_urls=job.get('query_urls'))
        query_urls = QuerySpider.query_urls
        reactor.stop()

runner = CrawlerRunner()
makerIds = ["16415"]
service = CosmosService()
lemon_spider_jobs = []
for mid in makerIds:
    maker = service.get_maker_by_id(mid)
    query_urls = []
    for m in maker.get('models'):
        for c in ['A', 'B', 'D', 'E', 'F', 'I', 'L', 'NL']:
            query_urls.append(f'https://www.autoscout24.de/lst/{quote(maker.get("name"))}/{quote(m.get("name"))}?cy={c}')
    lemon_spider_jobs.append({
        'maker': maker.get('name'),
        'query_urls': query_urls
    })

crawl(lemon_spider_jobs)
reactor.run()