from .crawler import Crawler
from .db import RedisClient
from .setting import POOL_UPPER_THRESHOLD

class Getter(object):
    """
    获取代理并向redis中添加
    """
    def __init__(self):
        self.redisClient = RedisClient()
        self.crawler = Crawler()

    def is_over_threshold(self):
        """
        判断是否达到了代理池容量限制
        :return: True: 达到限制，False：未达到限制
        """
        if self.redisClient.count() >= POOL_UPPER_THRESHOLD:
            return True
        else:
            return False

    def run(self):
        print("开始获取代理...")
        if self.is_over_threshold() == False:
            for callback_label in range(self.crawler.__CrawlFuncCount__):
                callback = self.crawler.__CrawlFunc__[callback_label]
                proxies = self.crawler.get_proxies(callback)
                for proxy in proxies:
                    self.redisClient.add(proxy)