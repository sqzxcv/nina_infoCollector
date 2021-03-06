"""
 根据命令行参数自动选择环境配置
"""
import sys

from . import default
from . import dev
from . import production


def singleton(cls):
    instance = cls()
    instance.__call__ = lambda: instance
    return instance


@singleton
class config(object):
    """
    default config
    """

    def __init__(self):
        """
        init
        """
        self._config = default.default.config()
        if self.isProduction_ENV:
            self._config = self.mergeDict(default.default.config(),
                                          production.production.config())
        else:
            self._config = self.mergeDict(default.default.config(),
                                          dev.develop.config())

    @property
    def info(self):
        return self._config

    @property
    def isProduction_ENV(self):
        if len(sys.argv) > 1 and sys.argv[1] == "production":
            return True
        else:
            return False

    def mergeDict(self, dict1, dict2):
        """
        两个 dict 合并
        """
        for key in dict2:
            dict1[key] = dict2[key]
        return dict1
