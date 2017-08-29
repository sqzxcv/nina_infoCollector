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
            "parsedocument": "http://localhost:8082/presedocument?url=",
            "scrapyDuration": 10 * 60,  # 爬虫运行多长时间后自动退出
            "fetchLength": 1,
            "Redis2Info": {
                "host": '127.0.0.1',
                "port": 6379,
                'pwd': "",
                'db': 2
            },
            "mysql": {
                "host": "localhost",
                "port": 3306,
                "user": "root",
                "pwd": "Anhuiqiang851",
                "db": "Nina",
            }
        }
