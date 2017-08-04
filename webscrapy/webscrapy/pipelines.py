# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


import codecs
import json
# from items import TitleSpiderItem
import threading
import sys
from string import Template
import pymysql as mdb
import time
# reload(sys)
# sys.path.append("..")
# import tools.Global as Global


class NewsSpiderPipeline(object):
    lock = threading.Lock()
    # file = open(Global.content_dir, 'a')

    def __init__(self):
        pass

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + '\n'
        try:
            NewsSpiderPipeline.lock.acquire()
            self.saveItem2db(item)
            # NewsSpiderPipeline.file.write(line)
        except:
            pass
        finally:
            NewsSpiderPipeline.lock.release()
        return item

    def spider_closed(self, spider):
        pass

    def saveItem2db(self, item):
        conn = mdb.connect(host='127.0.0.1', port=3306, user='root',
                           passwd='Anhuiqiang85!', db='nina', charset='utf8')
        cursor = conn.cursor()
        try:
            sqltemp = Template("insert into document(url,content,news_time,contentHtml,title,collect_time,audio) values('$url','$content',$news_time,'$contentHtml','$title',$collect_time,'$audio') ON DUPLICATE KEY UPDATE content= '$content', news_time=$news_time,contentHtml='$contentHtml',title='$title',collect_time=$collect_time, audio = '$audio'")
            # print "ceshi biaoti----title" + itemtitle
            sql = sqltemp.substitute(title=item["title"], url=item["url"], content=item["content"], contentHtml=item["content"],
                                     news_time=self.convertTimeFromString(item["time"]), audio = item['audio'], collect_time=int(time.time()))
            # print "~~~~~~~~~~~~~~sql=" + sql
            cursor.execute(sql)
            print ("插入新闻:{0}".format(item['title']))
            conn.commit()
        except:
            import traceback
            traceback.print_exc()
            conn.rollback()
        finally:
            cursor.close()
            conn.close()

    def convertTimeFromString(self, timestr):
        frmat = ""
        if len(timestr) == 0:
            return 0
        elif len(timestr) <= 4:
            frmat = "%Y"
        elif len(timestr) <= 7:
            frmat = "%Y-%m"
        elif len(timestr) <= 10:
            frmat = "%Y-%m-%d"
        elif len(timestr) <= 13:
            frmat = "%Y-%m-%d %H"
        elif len(timestr) <= 16:
            frmat = "%Y-%m-%d %H:%M"
        elif len(timestr) <= 19:
            frmat = "%Y-%m-%d %H:%M:%S"
        return time.mktime(time.strptime(timestr, frmat))


