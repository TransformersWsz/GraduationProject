import redis
from random import choice

from .error import PoolEmptyError
from .setting import REDIS_HOST, REDIS_PORT, REDIS_PASSWORD, REDIS_KEY
from .setting import MAX_SCORE, MIN_SCORE, INITIAL_SCORE


class RedisClient(object):
    def __init__(self, host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD):
        """
        初始化
        :param host: Redis 服务器地址
        :param port: Redis 连接端口
        :param password: Redis 授权密码
        """
        self.db = redis.StrictRedis(host=host, port=port, password=password, decode_responses=True)

    def add(self, proxy, score=INITIAL_SCORE):
        """
        添加新代理，设置初始分数为10
        :param proxy: 新代理
        :param score: 分数
        :return: 添加结果
        """
        if not self.db.zscore(REDIS_KEY, proxy):
            return self.db.zadd(REDIS_KEY, {proxy: score})

    def random(self):
        """
        随机获取有效代理，首先尝试获取最高分数代理，如果最高分数不存在，则按照排名获取，否则抛出异常
        :return: 随机代理
        """
        result = self.db.zrangebyscore(REDIS_KEY, MAX_SCORE, MAX_SCORE)
        if len(result):
            return choice(result)
        else:
            result = self.db.zrevrange(REDIS_KEY, MIN_SCORE, MAX_SCORE)
            if len(result):
                return choice(result)
            else:
                try:
                    raise PoolEmptyError("代理为空，找不到有用代理。")
                except PoolEmptyError as error:
                    print(error)

    def decrease(self, proxy):
        """
        代理值减1分，分数小于最小值，则去除该代理
        :param proxy: 代理
        :return: 修改之后的代理分数
        """
        score = self.db.zscore(REDIS_KEY, proxy)
        if score > MIN_SCORE:
            return self.db.zincrby(REDIS_KEY, proxy, -1)
        else:
            print("{proxy}当前代理不可用，将其去除".format(proxy=proxy))
            return self.db.zrem(REDIS_KEY, proxy)

    def exist(self, proxy):
        """
        判断该代理是否在代理池中
        :param proxy: 代理
        :return: True: 存在，False：不存在
        """
        return not self.db.zscore(REDIS_KEY, proxy) == None

    def max(self, proxy):
        """
        将代理分数设为最大值
        :param proxy: 代理
        :return: 设置结果
        """
        print("{proxy}可用，分数设置最大值{max_score}".format(proxy=proxy, max_score=MAX_SCORE))
        return self.db.zadd(REDIS_KEY, {proxy: MAX_SCORE})

    def count(self):
        """
        获取代理池的代理数量
        :return: 总数
        """
        return self.db.zcard(REDIS_KEY)

    def all(self):
        """
        获取全部代理
        :return: 全部代理
        """
        return self.db.zrangebyscore(REDIS_KEY, MIN_SCORE, MAX_SCORE)

    def batch(self, start, stop):
        """
        批量获取
        :param start: 开始索引
        :param stop: 结束索引
        :return: 代理列表
        """
        return self.db.zrevrange(REDIS_KEY, start, stop - 1)