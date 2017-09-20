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
from tools.logger import *
from config import config
# reload(sys)
# sys.path.append("..")
# import tools.Global as Global


class NewsSpiderPipeline(object):
    lock = threading.Lock()
    # file = open(Global.content_dir, 'a')
    mysql = config.info["mysql"]

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
        conn = mdb.connect(host=self.mysql["host"], port=self.mysql["port"],
                           user=self.mysql["user"], passwd=self.mysql["pwd"],
                           db=self.mysql["db"], charset='utf8')
        cursor = conn.cursor()
        sql = ""
        try:
            longStr = "insert into kejilie_raw_data(source, thumbnail, tags,url,content,news_time,contentHtml,title,collect_time) values($source, $thumbnail, $tags,$url,$content,$news_time,$contentHtml,$title,$collect_time) ON DUPLICATE KEY UPDATE content= $content, news_time=$news_time,contentHtml=$contentHtml,title=$title,collect_time=$collect_time, source=$source, thumbnail=$thumbnail, tags=$tags"
            sqltemp = Template(longStr)
            sql = sqltemp.substitute(title=conn.escape(item["title"]),
                                     url=conn.escape(item["url"]),
                                     content=conn.escape(item["content"]),
                                     contentHtml=conn.escape(item["content"]),
                                     news_time=self.convertTimeFromString(
                                         item["time"]),
                                     collect_time=int(time.time()),
                                     source=conn.escape(item['source']), thumbnail=conn.escape(item['thumbnail']), tags=conn.escape(item['tags']))
            cursor.execute(sql)
            dataid = int(conn.insert_id())
            info("插入新闻:{0}--[{1}]--{2}".format(item['time'], dataid,item['title']))
            conn.commit()
            longStr = "insert ignore into catalogs(name, logo) values($name, $logo)"
            sqltemp = Template(longStr)
            sql = sqltemp.substitute(
                name=conn.escape(item['catalog']['title']), logo=conn.escape(item['catalog']['logo']))
            cursor.execute(sql)
            catalogid = int(conn.insert_id())
            # debug("插入类目：「{0}」，id：「{1}」".format(item['catalog']['title'], item['catalog']['logo']))
            conn.commit()
            
            longStr = "insert ignore into catalogmap(sourceid, catalogid) values($sourceid, $catalogid)"
            sqltemp = Template(longStr)
            sql = sqltemp.substitute(
                sourceid=dataid, catalogid=catalogid)
            cursor.execute(sql)
            conn.commit()

        except:
            import traceback
            info("-------------sql:"+ sql);
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
