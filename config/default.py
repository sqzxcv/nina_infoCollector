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
            "scrapyDuration": 1 * 60  # 爬虫运行多长时间后自动退出
        }
