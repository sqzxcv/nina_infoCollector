#!/usr/bin/python
# coding: utf-8

import logging
import logging.config

LogPath = None
logger_name = "NINA"
loglevel = logging.DEBUG
fmt = "[%(name)s][%(levelname)s] %(asctime)s %(filename)s[%(lineno)s]    %(message)s"
datefmt = "%Y-%m-%d %Y %H:%M:%S"

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
        'streamHandler': {
            "class": "logging.StreamHandler",
            "formatter": "myFormatter"
        }
    },
    "loggers": {
        "App": {
            "handlers": ["streamHandler"],  # ["fileHandler", "streamHandler"],
            "level": "INFO",
        }
    },

    "formatters": {
        "myFormatter": {
            "format": "[%(name)s] [%(levelname)s]  %(asctime)s %(filename)s[%(lineno)s]    %(message)s"
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
        # logging.config.dictConfig(dictLogConfig)
        sh = logging.StreamHandler(stream=None)
        print("$$$$$$$$$$$$*******init NinaLogger******$$$$$$$$$$$$$$$$$")
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(loglevel)
        logFormat = logging.Formatter(fmt, datefmt)
        sh.setFormatter(logFormat)
        self.logger.addHandler(sh)


debug = NinaLogger.logger.debug
info = NinaLogger.logger.info
warning = NinaLogger.logger.warn
error = NinaLogger.logger.error
critical = NinaLogger.logger.critical
