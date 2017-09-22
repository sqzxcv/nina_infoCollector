"""
default config
"""


class default(object):
    """
    default config
    """

    @staticmethod
    def config():
        """
        default config
        """
        return {
            # "parsedocument": "http://localhost:8082/presedocument?url=",
            "parsedocument": "http://116.62.195.14:1082/presedocument?url=",
            "scrapyDuration": 10 * 60,  # 爬虫运行多长时间后自动退出
            "fetchLength": "1天前",  # "1月前",  # 提取 最近一个月的消息
            "Redis2Info": {
                "host": '127.0.0.1',
                "port": 6379,
                'pwd': "",
                'db': 2
            },
            "mysql": {
                # "host": "localhost",
                # "port": 3306,
                # "user": "root",
                # "pwd": "Anhuiqiang851",
                # "host": "116.62.195.14",
                "host": "123.207.79.244",
                "port": 3310,
                "user": "admin",
                "pwd": "Anhuiqiang85!",
                "db": "Nina",
            }
        }
