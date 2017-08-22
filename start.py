from apscheduler.schedulers.blocking import BlockingScheduler
# from redis import StrictRedis
# from webscrapy.webscrapy.webscrapySettings import Redis2Info
# import json
# import requests
# from sanic import Sanic
# from sanic.response import text
# from sanic import response
# from webscrapy.webscrapy.text2speech import text2speech
from logger import *

def fetchContentJob():
    # print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print ("++++++++++++++++++++启动爬虫kejilieChannelsContent爬去内容")
    res = requests.post("http://localhost:6800/schedule.json?spider=kejilieChannelsContent&&project=webscrapy")
    print ("++++++++++++++++++++" + res.text)

def fetchChannelsjob():
    print ('++++++++++++++++++++启动爬虫kejilieChannels爬取最新频道')
    res = requests.post("http://localhost:6800/schedule.json?project=webscrapy&&spider=kejilieChannels")
    print ("++++++++++++++++++++" + res.text)

# NinaLogger()
LogPath = "test"
info("this is test")

BlockingScheduler
scheduler = BlockingScheduler()
fetchContentJob()
scheduler.add_job(fetchContentJob, 'interval', hours=1)
scheduler.add_job(fetchChannelsjob, 'interval', days=7)
scheduler.start()

# app = Sanic(__name__)

# @app.route("/readContentWithURL",methods=['GET'])
# async def readContentWithURL(request):
#     url = request.args.get('url')
#     print("开始解析:" + url)
#     if len(url) != 0:
#         res = requests.get(
#             "http://localhost:3082/presedocument?url=" + url)
#         dict = res.json()
#         try:
#             audio = text2speech(dict['content'])
#             if audio != None:
#                 print("---------title===" + dict["title"] + "======audio====" + audio)
#                 dict['audio'] = audio
#                 dict['status'] = 200
#             else:
#                 msg("生成音频失败")
#                 dict['status'] = 0
#                 dict['msg'] = '音频生成失败'
#         except:
#             print("生成音频失败")
#             dict['status'] = 0
#             dict['msg'] = '音频生成失败'
#         finally:
#             return response.json(dict);
#     else:
#         info = {"status":-1,'msg':'参数错误'}
#         return response.json(info);

# if __name__ == "__main__":
#     app.run(port=3084)


