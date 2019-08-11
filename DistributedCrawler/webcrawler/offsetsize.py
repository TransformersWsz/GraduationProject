import time
import redis
from random import choice

from proxypool.setting import *

class Offsetsize(object):
    """
    获取爬取的偏移量和页大小
    """
    def __init__(self):
        super().__init__()
        self.redisClient = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, decode_responses=True)


    def get_offset_size(self):
        """
        获取offset和size
        :return: (offset, size)
        """
        result = self.redisClient.zrangebyscore(LOCK_KEY, 20, 20)
        if len(result):
            offset = choice(result)
            self.redisClient.zrem(LOCK_KEY, offset)
            return (offset, 20)
        else:
            return (0, 0)

    def concurrent_control_get_offset_size(self):
        """
        并发控制下的 get_offset_size
        :return: (offset, size)
        """
        lock_res = 0
        # 获取锁
        while lock_res != 1:
            now = int(time.time())
            lock_timeout = now + LOCK_TIMEOUT + 1
            lock_res = self.redisClient.setnx(LOCK_NAME, lock_timeout)
            if lock_res == 1:
                break
            else:
                old_expire_time = self.redisClient.get(LOCK_NAME)
                if now > old_expire_time:
                    current_expire_time = self.redisClient.getset(LOCK_NAME, lock_timeout)
                    if old_expire_time == current_expire_time:
                        break
                    else:
                        time.sleep(0.01)
                else:
                    time.sleep(0.01)

        # 执行业务逻辑
        result = self.get_offset_size()

        # 释放锁
        now = int(time.time())
        if now < lock_timeout:
            self.redisClient.delete(LOCK_NAME)

        return result

if __name__ == "__main__":
    offsetSize = Offsetsize()
    while True:
        s = input("input: \n")
        if s == "1":
            print(offsetSize.concurrent_control_get_offset_size())
        else:
            break



