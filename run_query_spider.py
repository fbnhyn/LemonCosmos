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
        "id": "47"
    },
    {
        "id": "74"
    },
    {
        "id": "13"
    },
    {
        "id": "9"
    },
    {
        "id": "29"
    },
    {
        "id": "54"
    },
    {
        "id": "65"
    },
    {
        "id": "51539"
    },
    {
        "id": "16396"
    },
    {
        "id": "14979"
    },
    {
        "id": "16429"
    },
    {
        "id": "16356"
    },
    {
        "id": "16352"
    },
    {
        "id": "6"
    },
    {
        "id": "14"
    },
    {
        "id": "51796"
    },
    {
        "id": "51545"
    },
    {
        "id": "16419"
    },
    {
        "id": "16427"
    },
    {
        "id": "16431"
    },
    {
        "id": "8"
    },
    {
        "id": "15643"
    },
    {
        "id": "15644"
    },
    {
        "id": "51774"
    },
    {
        "id": "16400"
    },
    {
        "id": "16416"
    },
    {
        "id": "11"
    },
    {
        "id": "16418"
    },
    {
        "id": "16424"
    },
    {
        "id": "16367"
    },
    {
        "id": "15"
    },
    {
        "id": "16"
    },
    {
        "id": "16379"
    },
    {
        "id": "17"
    },
    {
        "id": "15672"
    },
    {
        "id": "16407"
    },
    {
        "id": "16335"
    },
    {
        "id": "16401"
    },
    {
        "id": "16357"
    },
    {
        "id": "16384"
    },
    {
        "id": "19"
    },
    {
        "id": "20"
    },
    {
        "id": "21"
    },
    {
        "id": "16411"
    },
    {
        "id": "16380"
    },
    {
        "id": "51802"
    },
    {
        "id": "16360"
    },
    {
        "id": "22"
    },
    {
        "id": "16333"
    },
    {
        "id": "23"
    },
    {
        "id": "16397"
    },
    {
        "id": "16434"
    },
    {
        "id": "16423"
    },
    {
        "id": "51779"
    },
    {
        "id": "51773"
    },
    {
        "id": "2152"
    },
    {
        "id": "16339"
    },
    {
        "id": "16383"
    },
    {
        "id": "16415"
    },
    {
        "id": "51552"
    },
    {
        "id": "51794"
    },
    {
        "id": "16436"
    },
    {
        "id": "51831"
    },
    {
        "id": "27"
    },
    {
        "id": "28"
    },
    {
        "id": "51543"
    },
    {
        "id": "51542"
    },
    {
        "id": "16337"
    },
    {
        "id": "16386"
    },
    {
        "id": "16403"
    },
    {
        "id": "51540"
    },
    {
        "id": "51791"
    },
    {
        "id": "16421"
    },
    {
        "id": "2153"
    },
    {
        "id": "51813"
    },
    {
        "id": "16382"
    },
    {
        "id": "16409"
    },
    {
        "id": "51512"
    },
    {
        "id": "51534"
    },
    {
        "id": "51816"
    },
    {
        "id": "31"
    },
    {
        "id": "15674"
    },
    {
        "id": "51767"
    },
    {
        "id": "33"
    },
    {
        "id": "16355"
    },
    {
        "id": "15629"
    },
    {
        "id": "16402"
    },
    {
        "id": "35"
    },
    {
        "id": "14882"
    },
    {
        "id": "16387"
    },
    {
        "id": "37"
    },
    {
        "id": "38"
    },
    {
        "id": "39"
    },
    {
        "id": "51781"
    },
    {
        "id": "50060"
    },
    {
        "id": "40"
    },
    {
        "id": "41"
    },
    {
        "id": "42"
    },
    {
        "id": "15641"
    },
    {
        "id": "16426"
    },
    {
        "id": "43"
    },
    {
        "id": "16393"
    },
    {
        "id": "16353"
    },
    {
        "id": "14890"
    },
    {
        "id": "44"
    },
    {
        "id": "16359"
    },
    {
        "id": "51780"
    },
    {
        "id": "16435"
    },
    {
        "id": "16410"
    },
    {
        "id": "45"
    },
    {
        "id": "51803"
    },
    {
        "id": "16348"
    },
    {
        "id": "46"
    },
    {
        "id": "51519"
    },
    {
        "id": "16399"
    },
    {
        "id": "48"
    },
    {
        "id": "16361"
    },
    {
        "id": "51766"
    },
    {
        "id": "16338"
    },
    {
        "id": "50"
    },
    {
        "id": "51782"
    },
    {
        "id": "51"
    },
    {
        "id": "16388"
    },
    {
        "id": "51554"
    },
    {
        "id": "51788"
    },
    {
        "id": "52"
    },
    {
        "id": "53"
    },
    {
        "id": "15670"
    },
    {
        "id": "16341"
    },
    {
        "id": "51553"
    },
    {
        "id": "55"
    },
    {
        "id": "50083"
    },
    {
        "id": "16350"
    },
    {
        "id": "51770"
    },
    {
        "id": "51817"
    },
    {
        "id": "56"
    },
    {
        "id": "57"
    },
    {
        "id": "15636"
    },
    {
        "id": "15646"
    },
    {
        "id": "51793"
    },
    {
        "id": "51812"
    },
    {
        "id": "16398"
    },
    {
        "id": "60"
    },
    {
        "id": "61"
    },
    {
        "id": "62"
    },
    {
        "id": "51536"
    },
    {
        "id": "63"
    },
    {
        "id": "16369"
    },
    {
        "id": "64"
    },
    {
        "id": "51827"
    },
    {
        "id": "51800"
    },
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
# makerIds = ["13"]
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