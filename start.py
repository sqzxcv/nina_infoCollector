from apscheduler.schedulers.blocking import BlockingScheduler
from redis import StrictRedis
from webscrapy.webscrapy.webscrapySettings import Redis2Info
import json
import requests
    




def fetchContentJob():
    # print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print ("++++++++++++++++++++启动爬虫kejilieChannelsContent爬去内容")
    res = requests.post("http://localhost:6800/schedule.json?spider=kejilieChannelsContent&&project=webscrapy")
    print ("++++++++++++++++++++" + res.text)

def fetchChannelsjob():
    print ('++++++++++++++++++++启动爬虫kejilieChannels爬取最新频道')
    res = requests.post("http://localhost:6800/schedule.json?project=webscrapy&&spider=kejilieChannels")
    print ("++++++++++++++++++++" + res.text)


# BlockingScheduler
scheduler = BlockingScheduler()
fetchContentJob()
scheduler.add_job(fetchContentJob, 'interval', hours=1)
scheduler.add_job(fetchChannelsjob, 'interval', days=7)
scheduler.start()


