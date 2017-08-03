#!/usr/bin/env python
# encoding=utf-8

import requests
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor as SgmlLinkExtractor
from webscrapy.items import NewsSpiderItem
from webscrapy.webscrapySettings import Redis2Info
from redis import StrictRedis


class KejijieSpider(CrawlSpider):

    db = StrictRedis(
        host=Redis2Info['host'],
        port=Redis2Info['port'],
        password=Redis2Info['pwd'],
        db=Redis2Info['db']
    )
    urllist = db.smembers("kejiliechannels")
    start_urls = []
    for url in urllist:
        start_urls.append(url.decode('utf-8'))
        
    # start_urls = ['http://www.kejilie.com', "http://www.kejilie.com/channelsubscribe.html"]
    name = 'kejilie'
    allowed_domains = ['www.kejilie.com']
    rules = (Rule(SgmlLinkExtractor(allow=('http://www.kejilie.com/.*', )),
                  callback='parsepage', follow=True),)

    def parsepage(self, response):
        print("-----------------page url:" + response.url)
        urlparse = "http://localhost:8082/presedocument?url=" + response.url
        print("------urlparse:"+urlparse)
        res = requests.get(
            "http://localhost:8082/presedocument?url=" + response.url)
        dict = res.json()
        item = NewsSpiderItem()
        item["time"] = dict['news_times']
        item["title"] = dict["title"]
        item["content"] = dict["content"]
        item["url"] = response.url
        print("---------title===" + dict["title"] +"======")
        return item
