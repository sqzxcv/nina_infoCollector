#!/usr/bin/env python
# encoding=utf-8

import scrapy
from webscrapy.items import NewsSpiderItem
from webscrapy.webscrapySettings import Redis2Info
from webscrapy import webscrapySettings as wbsettings
from webscrapy.text2speech import text2speech
from redis import StrictRedis
import requests
from urllib.parse import urlparse


class kejilieChannelsContentSpider(scrapy.Spider):

    name = "kejilieChannelsContent"
    db = StrictRedis(
        host=Redis2Info['host'],
        port=Redis2Info['port'],
        password=Redis2Info['pwd'],
        db=Redis2Info['db']
    )
    urllist = db.smembers("kejiliechannels")
    start_urls = ['http://www.kejilie.com']
    channelsUrls = []
    for url in urllist:
        channelsUrls.append(url.decode('utf-8'))
    allowed_domains = ['www.kejilie.com']

    def parse(self, response):

        for url in self.channelsUrls:
            for index in range(0, wbsettings.fetchLength):
                pageurl = url[:-5] + "/" + str(index) + ".html"
                yield scrapy.Request(pageurl, self.parseList)

    def parseList(self, response):
        """
        获取文中 URL 链接
        """
        urls = response.xpath("//a/@href").extract()
        for url in urls:
            parse = urlparse(url)
            if 'http' == parse.scheme and parse.netloc in self.allowed_domains:
                yield scrapy.Request(url, self.parseNews)

    def parseNews(self, response):
        """
        提取网页正文等信息
        """
        print("-----------------page url:" + response.url)
        res = requests.get(
            "http://localhost:3082/presedocument?url=" + response.url)
        dict = res.json()
        item = NewsSpiderItem()
        item["time"] = dict['news_times']
        item["title"] = dict["title"]
        item["content"] = dict["content"]
        item["url"] = response.url
        item['audio'] = text2speech(item['content'])
        print("---------title===" + dict["title"] + "======audio====" + item['audio'])
        return item
