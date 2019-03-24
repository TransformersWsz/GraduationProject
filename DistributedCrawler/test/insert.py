import redis
from proxypool.setting import *

TOTAL = 1932
REDIS_KEY_NAME = "pages"

def insert():
    redisClient = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, decode_responses=True)

    nums = int(1932/20) + 1
    for i in range(0, nums):
        mapping = {str(i*20): 20}
        redisClient.zadd(REDIS_KEY_NAME, mapping)
        print(mapping)

if __name__ == "__main__":
    insert()

