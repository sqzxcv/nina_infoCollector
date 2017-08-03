from apscheduler.schedulers.blocking import BlockingScheduler
from redis import StrictRedis
from webscrapy.webscrapy.webscrapySettings import Redis2Info
import json

db = StrictRedis(
    host=Redis2Info['host'],
    port=Redis2Info['port'],
    password=Redis2Info['pwd'],
    db=Redis2Info['db']
)
channelsUrls = []

fileread =  open("urllist.txt", 'r')
jsonstr = fileread.read()
channelsUrls = json.loads(jsonstr)
# db.sadd("kejiliechannels", channelsUrls)
for url in channelsUrls:
    db.sadd("kejiliechannels", url)
    




# def job():
#     # print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
#     pass


# # BlockingScheduler
# scheduler = BlockingScheduler()
# scheduler.add_job(job, 'interval', hour=1)
# scheduler.start()
