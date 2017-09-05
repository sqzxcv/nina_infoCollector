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
            "parsedocument": "http://localhost:3082/presedocument?url=",
            "scrapyDuration": 40 * 60,
            "fetchLength": 1,
            "mysql": {
                "host": "localhost",
                "port": 3306,
                "user": "root",
                "pwd": "Anhuiqiang85!",
                "db": "Nina",
            }
        }
