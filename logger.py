#!/usr/bin/python
# coding: utf-8

import logging
import logging.config

LogPath = None

dictLogConfig = {
    "version": 1,
    "handlers": {
        # "fileHandler": {
        #     "class": "logging.FileHandler",
        #     "formatter": "myFormatter",
        #     "filename": "logs/logger_test.txt"
        # },
        # "rotatingFileHandler":{
        #     "class":"logging.handlers.RotatingFileHandler",
        #     "formatter": "myFormatter",
        #     "filename": "logger_test.txt",
        #     "maxBytes":1024*1024*2,
        #     "backupCount":40
        # },
        'streamHandler':{
            "class":"logging.StreamHandler",
            "formatter":"myFormatter"
        }
    },
    "loggers": {
        "App": {
            "handlers":["streamHandler"],# ["fileHandler", "streamHandler"],
            "level": "INFO",
        }
    },

    "formatters": {
        "myFormatter": {
            "format": "[%(levelname)s]  %(asctime)s %(filename)s[%(lineno)s]    %(message)s"
        }
    }
}

def singleton(cls):
    instance = cls()
    instance.__call__ = lambda: instance
    return instance

@singleton
class NinaLogger(object):
    logger = None
    def __init__(self):
        logging.config.dictConfig(dictLogConfig)
        self.logger = logging.getLogger("App")


debug = NinaLogger.logger.debug
info = NinaLogger.logger.info
warning = NinaLogger.logger.warn
error = NinaLogger.logger.error
critical = NinaLogger.logger.critical

# import logging
# from logging import *
# from datetime import *

# logger = logging.getLogger()
# logger.setLevel(logging.DEBUG)

# handler = logging.FileHandler("reindex_out.log", 'a')
# fmt = logging.Formatter("[%(levelname)s]%(asctime)s %(filename)s[%(lineno)s] \
# : %(message)s", "%Y-%m-%d %H:%M:%S")
# handler.setFormatter(fmt)
# logger.addHandler(handler)

# debug = logger.debug
# info = logger.info
# warning = logger.warn
# error = logger.error
# critical = logger.critical

# -*- encoding:utf-8 -*-
# import logging
# import logging.config

# def initLogging:
#     logging.config.fileConfig("./logging.conf")

# # create logger
# logger_name = "example"
# logger = logging.getLogger(logger_name)
