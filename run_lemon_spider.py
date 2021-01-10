import getopt
import sys
from scrapy.crawler import CrawlerProcess
from lmpd.lemon.lemon.spiders.lemon_spider import LemonSpider

# enter array of makers
# for each maker, load all models from db
# create array of query_urls /<maker>/<model>

# makerIds = ["16415"]
# makerName = []
# makerModelQueryObjects = []
# for makerId in makerName:
#     makerModels = 
#     for makerModel in makerModels:
#         makerModelQueryObjects.append({
#             maker:
#         })

process = CrawlerProcess()
process.crawl(LemonSpider)
process.start()