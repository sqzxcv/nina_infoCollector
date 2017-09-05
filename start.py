
from apscheduler.schedulers.background import BackgroundScheduler
from scrapy import cmdline
import logging

from config import config
from tools.logger import info, NinaLogger

# config.info


def fetchContentJob():
    """
    fetchContentJob
    """
    info('++++++++++++++++++++启动爬虫kejilieChannelsContent爬取最新内容')
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
    # 设置 级别logs
    # if config.isProduction_ENV:
    #     logging.getLogger("requests").setLevel(logging.WARNING)
    logging.getLogger("requests").setLevel(logging.WARNING)
    NinaLogger.logger.setLevel(logging.INFO)
    scheduler = BackgroundScheduler()
    scheduler.add_job(fetchContentJob, 'interval', hours=1)
    scheduler.start()
    fetchContentJob()

# BlockingScheduler
# scheduler.add_job(fetchChannelsjob, 'interval', days=7)
# scheduler.start()


if __name__ == '__main__':
    main()
