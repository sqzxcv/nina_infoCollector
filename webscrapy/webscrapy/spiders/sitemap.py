from scrapy.spiders import SitemapSpider
from webscrapy.webscrapy.items import NewsSpiderItem
import requests


class sitemap(SitemapSpider):
    sitemap_urls = ["http://www.kejilie.com/sitemap.xml"]
    name = "sitemap"

    def parse(self, response):
        print("-----------------page url:" + response.url)
        urlparse = "http://localhost:8082/presedocument?url=" + response.url
        print("------urlparse:" + urlparse)
        res = requests.get(
            "http://localhost:8082/presedocument?url=" + response.url)
        dict = res.json()
        item = NewsSpiderItem()
        item["time"] = dict['news_times']
        item["title"] = dict["title"]
        item["content"] = dict["content"]
        item["url"] = response.url
        print("---------title===" + dict["title"] + "======")
        return item
