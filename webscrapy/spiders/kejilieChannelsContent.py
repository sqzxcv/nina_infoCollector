#!/usr/bin/env python
# encoding=utf-8


import scrapy
from scrapy.exceptions import CloseSpider
from webscrapy.items import NewsSpiderItem
# import webscrapy.webscrapy.items.NewsSpiderItem as NewsSpiderItem
from redis import StrictRedis
import requests
from urllib.parse import urlparse
from tools.logger import info, debug
from config import config
import time
import re
import json


class kejilieChannelsContentSpider(scrapy.Spider):

    name = "kejilieChannelsContent"
    createtimer = time.time()
    Redis2Info = config.info["Redis2Info"]
    db = StrictRedis(
        host=Redis2Info['host'],
        port=Redis2Info['port'],
        password=Redis2Info['pwd'],
        db=Redis2Info['db']
    )
    # urllist = db.smembers("kejiliechannels")

    catalogs = db.smembers("kejiliechannels")
    start_urls = ['http://www.kejilie.com']
    channelsUrls = []
    allowed_domains = ['www.kejilie.com']
    didPitchOutUrlArray = []

    def parse(self, response):
        """
        提取文章类目
        """
        self.didPitchOutUrlArray = [] #开始新的爬起流程，记录清空
        for catalog_str in self.catalogs:
            catalog = json.loads(catalog_str)
            url = catalog['url']
            index = 0
            while True:
                if url not in self.didPitchOutUrlArray:
                    pageurl = url[:-5] + "/" + str(index) + ".html"
                    index = index + 1
                    debug("pith url[" + url +"] index:" + str(index -1))
                    yield scrapy.Request(pageurl, callback=self.parseList, meta={'catalog': catalog})
                else:
                    info("-----url" + url + " did pitch out------")
                    break

    def parseList(self, response):
        """
        获取文中 URL 链接，提取文章列表页面
        """
        li_items = response.xpath("//ul[@class='am-list']/li")
        for li_selector in li_items:
            li_time = li_selector.xpath(
                ".//span[@class='am_news_time']/time/text()").extract_first()
            fetchLength = self.dealTime(config.info["fetchLength"])
            if False:  # self.dealTime(li_time) < fetchLength:
                url = li_selector.xpath(
                    ".//h3[@class='am_list_title']/a/@href").extract()
                if 'http' == parse.scheme and parse.netloc in self.allowed_domains:
                    yield scrapy.Request(url, callback=self.parseNews, meta={'catalog': response.meta['catalog']})
            else:
                info("-----record url" + response.meta['catalog']['url'] + " finished------")
                self.didPitchOutUrlArray.append(response.meta['catalog']['url'])
                break

    def parseNews(self, response):
        """
        提取网页正文等信息
        """
        # title =
        # info("test")
        return ''
        if self.createtimer + config.info["scrapyDuration"] < time.time():
            raise CloseSpider("spider time out")  # time out 发送异常 关闭爬虫
            return None
        info("-----------------page url:" + response.url)
        res = requests.get(
            config.info['parsedocument'] + response.url)
        articles = response.xpath("//article")
        if len(articles) != 0:
            title = articles[0].xpath(
                ".//article//h1[@class='article_nr_title']/text()").extract_first()
            source = articles[0].xpath(
                ".//article//div[@class='am_list_author']/a/span[@class='name']/text()").extract_first()
            time = articles[0].xpath(
                ".//article//div[@class='am_list_author']/span[@class='am_news_time']/time[@title]/@title").extract_first()
            thumbnail = articles[0].xpath(
                './/div[@class="so-content"]//img/@src').extract_first()
            info('title:' + title + '------- time:' + time + "-------")
            # content = response.xpath('//div[@class="so-content"]//p/text()').extract()
            tags = articles[0].xpath(
                './/div[@class="so-content"]/a[@target="_blank"]/span/text()').extract()
            dict = res.json()
            item = NewsSpiderItem()
            item["time"] = time
            item["title"] = title
            item["content"] = dict["content"]
            item["url"] = response.url
            item.html = dict.contentHtml
            item.source = source
            item.thumbnail = thumbnail
            item.tags = json.dumps(tags)
            return item
        else:
            return ""

    def dealTime(self, time_str):
        """
        """
        nums = re.findall(r'\d+', time_str)
        if len(nums) == 0:
            return 0
        num = nums[0]
        # 毫秒
        pics = time_str[len(num):]
        oneLens = 0
        if pics is "分钟前":
            oneLens = 1000 * 60
        elif pics is "小时前":
            oneLens = 1000 * 60 * 60
        elif pics is "天前":
            oneLens = 1000 * 60 * 60 * 24
        elif pics is "周前":
            oneLens = 1000 * 60 * 60 * 24 * 7
        elif pics is "月前":
            oneLens = 1000 * 60 * 60 * 24 * 30
        elif pics is "年前":
            oneLens = 1000 * 60 * 60 * 24 * 365
        elif pics is "刚刚":
            oneLens = 1000

        return num * oneLens
