import time
from multiprocessing import Process
from .api import app
from .getter import Getter
from .tester import Tester
from .db import RedisClient
from .setting import *

class Scheduler(object):
    def schedule_tester(self, cycle=TESTER_CYCLE):
        """
        定时测试代理
        :param cycle: 周期
        :return: None
        """
        tester = Tester()
        while True:
            print("定时测试代理开始...")
            tester.run()
            time.sleep(cycle)

    def schedule_getter(self, cycle=GETTER_CYCLE):
        """
        定时获取代理
        :param cycle: 周期
        :return: None
        """
        getter = Getter()
        while True:
            print("定时抓取代理...")
            getter.run()
            time.sleep(cycle)

    def schedule_api(self):
        """
        开启api接口
        :return: None
        """
        app.run(API_HOST, API_PORT)

    def run(self):
        """
        调度器运行
        :return: None
        """
        print("调度器开始运行...")

        tester_process = Process(target=self.schedule_tester)
        tester_process.start()

        getter_process = Process(target=self.schedule_getter)
        getter_process.start()

        api_process = Process(target=self.schedule_api)
        api_process.start()
