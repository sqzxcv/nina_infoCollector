#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
通过 text2speech 将传入的 text 通过百度语音转换成 mp3,然后上传到七牛
"""

from pydub import AudioSegment
import time
import requests
import re
from urllib import parse
from qiniu import Auth, put_file
import os
import shutil
from tools.logger import info, debug, error

access_token = ""
expires_date = 0
qiniuAuth = ""


def text2speech(text):
    """
     return: 返回 通过text 转换成 的mp3音频文件路径,如果转换失败,返回 None
    """
    # re.split(r'[;,\s]\s*', line)
    # 采用捕获分组,在分割的结果集合中包含匹配结果,如果不需要匹配结果可以用数据集:r'[.?!,;。？！，、；]'
    splitArr = re.split(r'(\.|\?|!|,|;|。|？|！|，|、|；)', text)
    # info splitArr[0]
    textArr = []
    subtext = ""
    for substr in splitArr:
        if len(subtext + substr) > 300 and len(subtext) != 0:
            textArr.append(parse.quote(subtext))
            subtext = substr
            continue
        elif len(subtext + substr) > 300 and len(subtext) == 0:
            subtext += substr
            textArr.append(parse.quote(subtext))
            subtext = ""
        else:
            subtext += substr
    textArr.append(parse.quote(subtext))

    access_token = login()

    if len(access_token) == 0:
        error("百度语音 API token 为空")
    else:
        ttsurl = "http://tsn.baidu.com/text2audio?lan=zh&tok=" + \
            access_token + "&ctp=1&cuid=aaaaaaaaaaaa&tex="
        # silenceAudio = AudioSegment.silent(duration=10000)
        song = None
        dir = os.getcwd() + "/ttsdata/"
        if os.path.isdir(dir) is False:
            os.mkdir(dir)
        dir = dir + "ttsdata" + \
            str(int(time.time() * 100000000000000)) + "/"
        if os.path.isdir(dir) is False:
            os.mkdir(dir)
        textfilepath = dir + str(int(time.time()))
        i = 0
        for sbtext in textArr:
            url = ttsurl + sbtext
            res = requests.get(url)
            if res.headers['content-type'] == 'audio/mp3':
                # res.content
                filepath = textfilepath + "_" + str(i) + ".mp3"
                mp3fileobj = open(filepath, 'wb')
                mp3fileobj.write(res.content)
                songtmp = AudioSegment.from_mp3(filepath)
                if song is not None:
                    db1 = song.dBFS
                    db2 = songtmp.dBFS
                    dbplus = db1 - db2
                    if dbplus < 0:
                        song += abs(dbplus)
                    elif dbplus > 0:
                        songtmp += abs(dbplus)
                    song = song + songtmp
                else:
                    song = songtmp
                mp3fileobj.close()
            else:
                error("文本<" + sbtext + ">转换音频失败,错误原因:" + res.text())
                return None
            debug("生成 MP3文件:第" + str(i) + "碎片:" + parse.unquote(sbtext))
            i += 1
        resultPath = dir + "/res_" + str(int(time.time())) + ".mp3"
        song.export(resultPath, format="mp3")
        info("音频文件生成成功")
        uploadPath = uploadspeech(resultPath)
        if uploadPath is not None:
            shutil.rmtree(dir)
    return uploadPath


uploadspeechRetryCount = 0


def uploadspeech(localpath):
    """
    upload file to qiniu, if upload failed, it will retry 3 times.
    if upload still failed after retry, it return "None"
    """
    access_key = '_D2Iavhr-DRKHHhW0BTT7-liQ2jO-1cC_lqKn0eF'
    secret_key = 'E3QKF99mgA8HAyGF1nMlKWVVaKlIxRpTZvEb1CiO'
    global qiniuAuth
    if isinstance(qiniuAuth, Auth) is False:
        qiniuAuth = Auth(access_key, secret_key)
    bucket_name = 'pipixia'
    key = "audio_" + str(int(time.time())) + ".mp3"
    uptoken = qiniuAuth.upload_token(bucket_name, key, 700000)
    ret, info = put_file(uptoken, key, localpath)
    global uploadspeechRetryCount
    if ret is None:
        info(info)
        if uploadspeechRetryCount < 4:
            uploadspeechRetryCount += 1
            return uploadspeech(localpath)
        else:
            return None
    else:
        uploadspeechRetryCount = 0
        return "http://oty38yumz.bkt.clouddn.com/" + key


def login():
    """
    return access_token
    """
    global access_token
    global expires_date
    if expires_date > int(time.time()) and len(access_token) > 0:
        return access_token
    url = "https://openapi.baidu.com/oauth/2.0/token?grant_type=client_credentials&client_id=6NCOZQHM7f2bGzc9tKemZovU&client_secret=X0uXNGMIUkiockwY8Q16P6B41E3Xc98a&"
    resStr = requests.get(url)
    res = resStr.json()
    try:
        access_token = res["access_token"]
        expires_date = int(time.time()) + res["expires_in"] - 1000
        return access_token
    except:
        import traceback
        traceback.print_exc()
        error("获取百度 tts token 失败:" + resStr.text())
        access_token = ""
        expires_date = 0
        return ""
