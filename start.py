from apscheduler.schedulers.background import BackgroundScheduler
from logger import info
from twisted.internet import reactor
import scrapy
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.settings import Settings

# from webscrapy.webscrapy.spiders.kejilieChannels import kejilieChannels
from webscrapy.webscrapy.spiders.\
    kejilieChannelsContent import kejilieChannelsContentSpider
from config import config

# config.info


def fetchContentJob():
    """
    fetchContentJob
    """
    info("++++++++++++++++++++启动爬虫kejilieChannelsContent爬去内容")
    configure_logging(
        {'LOG_FORMAT': '[%(levelname)s]  %(asctime)s %(filename)s[%(lineno)s]    %(message)s'})
    settings = Settings()
    configure_logging(settings)
    settings.set("BOT_NAME", 'webscrapy')
    settings.set("ROBOTSTXT_OBEY", True)
    settings.set("DOWNLOAD_DELAY", 3)
    if config.isProduction_ENV:
        settings.set("DOWNLOADER_MIDDLEWARES", {
            'webscrapy.webscrapy.rotateuseragent.RotateUserAgentMiddleware': 400
        })
    settings.set("ITEM_PIPELINES", {
        'webscrapy.webscrapy.pipelines.NewsSpiderPipeline': 300,
    })
    # settings = {"DOWNLOADER_MIDDLEWARES": {
    #     'webscrapy.webscrapy.rotateuseragent.RotateUserAgentMiddleware': 400
    # },
    #     "ITEM_PIPELINES": {
    #     'webscrapy.webscrapy.pipelines.NewsSpiderPipeline': 300,
    # }}
    runner = CrawlerRunner(settings)
    d = runner.crawl(kejilieChannelsContentSpider)
    d.addBoth(lambda _: reactor.stop())
    reactor.run()  # the script will block here until the crawling is finished


def fetchChannelsjob():
    """
    fetchChannelsjob
    """
    info('++++++++++++++++++++启动爬虫kejilieChannels爬取最新频道')


def main():
    """
    main
    """
    scheduler = BackgroundScheduler()
    scheduler.add_job(fetchContentJob, 'interval', hours=1)
    scheduler.start()
    fetchContentJob()

# BlockingScheduler
# scheduler.add_job(fetchChannelsjob, 'interval', days=7)
# scheduler.start()


if __name__ == '__main__':
    main()
