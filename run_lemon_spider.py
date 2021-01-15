from lmpd.lemon.lemon.spiders.query_spider import QuerySpider
from urllib.parse import quote

from twisted.internet import defer, reactor
from lmpd.cosmos.service import CosmosService
from scrapy.crawler import CrawlerRunner

@defer.inlineCallbacks
def crawl(limen_spider_jobs):
    for job in limen_spider_jobs:
        # The maximum of python arrays is 536.870.912
        # query_urls is a class variable and has to be cleared for every QuerySpider
        QuerySpider.query_urls = []
        QuerySpider.combind_query_counter = 0
        yield runner.crawl(QuerySpider, start_urls=job.get('query_urls'))
        print(u for u in query_urls)
    reactor.stop()

runner = CrawlerRunner()
makerIds = ["21"]
service = CosmosService()
lemon_spider_jobs = []
for mid in makerIds:
    maker = service.get_maker_by_id(mid)
    query_urls = []
    for m in maker.get('models'):
        for c in ['A', 'B', 'D', 'E', 'F', 'I', 'L', 'NL']:
            query_urls.append(f'https://www.autoscout24.de/lst/{quote(maker.get("name"))}/{quote(m.get("name"))}?offer=u&cy={c}')
    lemon_spider_jobs.append({
        'maker': maker.get('name'),
        'query_urls': query_urls
    })

crawl(lemon_spider_jobs)
reactor.run()