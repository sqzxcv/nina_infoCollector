"""
production enviroment config
"""


class production(object):
    """
    production config
    """

    @staticmethod
    def config():
        """
        production config
        """
        return {
            "parsedocument": "http://116.62.195.14:1082/presedocument?url=",
            "scrapyDuration": 40 * 60,
            "fetchLength": "7天前",  #提取 最近一个月的消息
            "mysql": {
                "host": "47.52.88.82",
                "port": 3310,
                "user": "root",
                "pwd": "Anhuiqiang85!",
                "db": "Nina",
            }
        }
