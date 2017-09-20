
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from redis import StrictRedis

import sys
print(__file__ + ":")
print(sys.path)
from tools.logger import info
from config import config
import json


class KejijieChannelsSpider(CrawlSpider):

    start_urls = ["http://www.kejilie.com/channelsubscribe.html"]
    name = 'kejilieChannels'
    allowed_domains = ['www.kejilie.com']
    Redis2Info = config.info["Redis2Info"]
    redis_db = StrictRedis(
        host=Redis2Info['host'],
        port=Redis2Info['port'],
        password=Redis2Info['pwd'],
        db=Redis2Info['db']
    )
    rules = (Rule(LxmlLinkExtractor(allow=('http://www.kejilie.com/channeltype/.*', )),
                  follow=True),
             Rule(LxmlLinkExtractor(allow=('http://www.kejilie.com/channel/.*', ), deny=("http://www.kejilie.com/channel/.*/feed")),
                  callback='parseChannel')
             )

    def parseChannel(self, response):
        info("-----------------kejiliechannels url:" + response.url)
        title = response.xpath(
            "//div[@class='am_news_list_all']//div[@class='am-titlebar am-titlebar-default mt-0']/h1/text()").extract_first()
        logo = response.xpath(
            "//div[@class='am_news_list_all']//div[@class='mt-10']/div[@class='am-fl']/img/@src").extract_first()
        self.redis_db.sadd("kejiliechannels", json.dumps(
            {'url': response.url, 'title': title, 'logo': logo}))
