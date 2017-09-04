
from apscheduler.schedulers.background import BackgroundScheduler
from tools.logger import info
from twisted.internet import reactor
import scrapy
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.settings import Settings
from scrapy import cmdline

# from webscrapy.webscrapy.spiders.kejilieChannels import kejilieChannels
from webscrapy.spiders.\
    kejilieChannelsContent import kejilieChannelsContentSpider
from config import config
import os
import subprocess

# config.info


def fetchContentJob():
    """
    fetchContentJob
    """
    # scrapyCmd = ' scrapy crawl kejilieChannelsContent'  # "scrapy crawl kejilieChannelsContent > /dev/null 2>&1"
    # result = os.system(scrapyCmd)
    # result = subprocess.call(scrapyCmd, shell=True)
    # info(result)
    cmdline.execute("scrapy crawl kejilieChannelsContent".split(" "))


def fetchChannelsjob():
    """
    fetchChannelsjob
    """
    info('++++++++++++++++++++启动爬虫kejilieChannels爬取最新频道')


def main():
    """
    main
    """
    # scheduler = BackgroundScheduler()
    # scheduler.add_job(fetchContentJob, 'interval', hours=1)
    # scheduler.start()
    fetchContentJob()

# BlockingScheduler
# scheduler.add_job(fetchChannelsjob, 'interval', days=7)
# scheduler.start()


if __name__ == '__main__':
    main()
