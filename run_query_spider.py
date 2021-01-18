from datetime import datetime
from lmpd.lemon.lemon.spiders.query_spider import QuerySpider
from urllib.parse import quote

from twisted.internet import defer, reactor
from lmpd.cosmos.service import CosmosService
from scrapy.crawler import CrawlerRunner

@defer.inlineCallbacks
def crawl(limen_spider_jobs):
    for job in limen_spider_jobs:
        print(f'start crawling queries for {job.get("maker")}')
        QuerySpider.result.hits = 0
        QuerySpider.result.urls = []
        QuerySpider.result.time = datetime.now().isoformat()
        yield runner.crawl(QuerySpider, start_urls=job.get('query_urls'))
        service.append_query_result_to_maker(job.get('makerId'), QuerySpider.result)
        print(f'crawled queries for {job.get("maker")}')
    reactor.stop()


ids = [
    {
        "id": "15525"
    },
    {
        "id": "51538"
    },
    {
        "id": "16377"
    },
    {
        "id": "66"
    },
    {
        "id": "51795"
    },
    {
        "id": "67"
    },
    {
        "id": "68"
    },
    {
        "id": "51551"
    },
    {
        "id": "16404"
    },
    {
        "id": "16327"
    },
    {
        "id": "51557"
    },
    {
        "id": "51535"
    },
    {
        "id": "51520"
    },
    {
        "id": "16420"
    },
    {
        "id": "70"
    },
    {
        "id": "15633"
    },
    {
        "id": "16326"
    },
    {
        "id": "2120"
    },
    {
        "id": "16253"
    },
    {
        "id": "71"
    },
    {
        "id": "16389"
    },
    {
        "id": "51809"
    },
    {
        "id": "16385"
    },
    {
        "id": "16422"
    },
    {
        "id": "73"
    },
    {
        "id": "16336"
    },
    {
        "id": "51513"
    },
    {
        "id": "16351"
    },
    {
        "id": "16408"
    },
    {
        "id": "16394"
    },
    {
        "id": "51798"
    },
    {
        "id": "51807"
    },
    {
        "id": "16328"
    }
]

runner = CrawlerRunner()
makerIds = list(id.get('id') for id in ids)
service = CosmosService()
lemon_spider_jobs = []

for mid in makerIds:
    maker = service.get_maker_by_id(mid)
    query_urls = []

    for m in maker.get('models'):

        for c in ['A', 'B', 'D', 'E', 'F', 'I', 'L', 'NL']:
            query_urls.append(f'https://www.autoscout24.de/lst/{quote(maker.get("name"))}/{quote(m.get("name"))}?size=20&offer=U,u&cy={c}')

    lemon_spider_jobs.append({
        'makerId': mid,
        'maker': maker.get('name'),
        'query_urls': query_urls
    })

crawl(lemon_spider_jobs)
reactor.run()