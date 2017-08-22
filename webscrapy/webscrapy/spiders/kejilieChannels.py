import requests
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from webscrapy.webscrapy.webscrapySettings import Redis2Info
from redis import StrictRedis
from logger  import *


class KejijieChannelsSpider(CrawlSpider):

    start_urls = ["http://www.kejilie.com/channelsubscribe.html"]
    name = 'kejilieChannels'
    allowed_domains = ['www.kejilie.com']
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
        self.redis_db.sadd("kejiliechannels", response.url)
