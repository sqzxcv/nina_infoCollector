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
import time as CTimer
import re
import json


class kejilieChannelsContentSpider(scrapy.Spider):

    name = "kejilieChannelsContent"
    createtimer = CTimer.time()
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

    def parse(self, response):
        """
        提取文章类目
        """
        # idn = 0
        for catalog_str in self.catalogs:
            catalog = json.loads(catalog_str)
            url = catalog['url']
            catalog['index'] = 0
            # idn += 1
            # debug("catalogindex:" + str(idn))
            # if idn > 1:
            #     break
            yield scrapy.Request(url, callback=self.parseList, meta={'catalog': catalog})

    def parseList(self, response):
        """
        获取文中 URL 链接，提取文章列表页面
        """
        info('-----开始抓取类目：{0}-----'.format(response.meta['catalog']['title']))
        needPitchNextPage = True
        li_items = response.xpath("//ul[@class='am-list']/li")
        catalog = response.meta['catalog']
        if len(li_items) == 0:
            needPitchNextPage == False
            if catalog['index'] == 0:
                del catalog['index']
                self.db.srem(catalog)
            return None
        for li_selector in li_items:
            li_time = li_selector.xpath(
                ".//span[@class='am_news_time']/time/text()").extract_first()
            if li_time is None:
                continue
            # debug(li_time + "-------" + config.info["fetchLength"])
            fetchLength = self.dealTime(config.info["fetchLength"])
            if self.dealTime(li_time) < fetchLength:
                url = li_selector.xpath("//h3/a/@href").extract_first()
                if url is None:
                    info("2``````````````url" + response.url)
                    info("index:" + li_items.index(li_selector))
                    info("1``````````````url is None")
                parse = urlparse(url)
                if 'http' == parse.scheme and parse.netloc in self.allowed_domains:
                    yield scrapy.Request(url, callback=self.parseNews, meta={'catalog': response.meta['catalog']})
            else:
                # 本类目最新内容已经全部获取了
                info(
                    "-----------------------url[" + response.meta['catalog']['url'] + "] 爬虫完成")
                needPitchNextPage = False
                break

        if needPitchNextPage and (self.createtimer + config.info["scrapyDuration"]) > CTimer.time():
            url = catalog['url']
            index = catalog['index'] + 1
            pageurl = url[:-5] + "/" + str(index) + ".html"
            catalog['index'] = index
            info("-----pitch pageurl[" + pageurl + "]------")
            yield scrapy.Request(pageurl, callback=self.parseList, meta={'catalog': catalog})
        else:
            return None

    def parseNews(self, response):
        """
        提取网页正文等信息
        """
        # title =
        # info("test")
        if self.createtimer + config.info["scrapyDuration"] < CTimer.time():
            raise CloseSpider("spider time out")  # time out 发送异常 关闭爬虫
            return None
        # info("-----------------page url:" + response.url)
        res = requests.get(
            config.info['parsedocument'] + response.url)
        articles = response.xpath("//article")
        if len(articles) != 0:
            title = articles[0].xpath(
                ".//h1[@class='article_nr_title']/text()").extract_first()
            source = articles[0].xpath(
                ".//div[@class='am_list_author']/a/span[@class='name']/text()").extract_first()
            datatime = articles[0].xpath(
                ".//div[@class='am_list_author']/span[@class='am_news_time']/time[@title]/@title").extract_first()
            thumbnail = articles[0].xpath(
                './/div[@class="so-content"]//img/@src').extract_first()
            # info('title:' + title + '------- time:' + datatime + "-------")
            # content = response.xpath('//div[@class="so-content"]//p/text()').extract()
            tags = articles[0].xpath(
                './/div[@class="so-content"]/a[@target="_blank"]/span/text()').extract()
            dict = res.json()
            item = NewsSpiderItem()
            item["time"] = datatime
            item["title"] = title
            item["content"] = dict["content"]
            item["url"] = response.url
            item["html"] = dict["contentHtml"]
            item["source"] = source
            item['thumbnail'] = thumbnail
            item['tags'] = json.dumps(tags)
            item['catalog'] = response.meta['catalog']
            return item
        else:
            return None

    def dealTime(self, time_str):
        """
        """
        time_str = "".join(time_str.split())
        nums = re.findall(r'\d+', time_str)
        if len(nums) == 0:
            return 0
        num = nums[0]
        # 毫秒
        pics = time_str[len(num):]
        oneLens = 0
        if pics == "分钟前":
            oneLens = 1000 * 60
        elif pics == "小时前":
            oneLens = 1000 * 60 * 60
        elif pics == "天前":
            oneLens = 1000 * 60 * 60 * 24
        elif pics == "周前":
            oneLens = 1000 * 60 * 60 * 24 * 7
        elif pics == "月前":
            oneLens = 1000 * 60 * 60 * 24 * 30
        elif pics == "年前":
            oneLens = 1000 * 60 * 60 * 24 * 365
        elif pics == "刚刚":
            oneLens = 1000

        return int(num) * oneLens
