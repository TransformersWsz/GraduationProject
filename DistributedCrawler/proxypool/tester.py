import sys
import time
import aiohttp
import asyncio
from aiohttp import ClientError
from .db import RedisClient
from .setting import *

class Tester(object):
    def __init__(self):
        self.redisClient = RedisClient()

    async def test_single_proxy(self, proxy):
        """
        测试单个代理
        :param proxy: 代理
        :return: None
        """
        conn = aiohttp.TCPConnector(verify_ssl=False)
        async with aiohttp.ClientSession(connector=conn) as session:
            try:
                real_proxy = "http://" + proxy
                async with session.get(TEST_URL, proxy=real_proxy, timeout=15) as response:
                    if response.status in VALID_STATUS_CODES:
                        self.redisClient.max(proxy)
                        print("{proxy}可用".format(proxy=proxy))
                    else:
                        self.redisClient.decrease(proxy)
                        print("{proxy}代理不合法".format(proxy=proxy))
            except (ClientError, aiohttp.client_exceptions.ClientConnectorError, asyncio.TimeoutError,
                    AttributeError):
                self.redisClient.decrease(proxy)
                print('代理请求失败', proxy)

    def run(self):
        """
        测试主函数
        :return: None
        """
        print('测试器开始运行...')
        try:
            count = self.redisClient.count()
            for i in range(0, count, BATCH_TEST_SIZE):
                start = i
                stop = min(i + BATCH_TEST_SIZE, count)
                print('正在测试第', start + 1, '-', stop, '个代理')
                test_proxies = self.redisClient.batch(start, stop)
                loop = asyncio.get_event_loop()
                tasks = [self.test_single_proxy(proxy) for proxy in test_proxies]
                loop.run_until_complete(asyncio.wait(tasks))
                sys.stdout.flush()
                time.sleep(5)
        except Exception as e:
            print('测试器发生错误', e.args)
