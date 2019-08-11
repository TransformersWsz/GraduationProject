import requests

from .log import Log
from .offsetsize import Offsetsize
from mysqldb.dao import MysqlClient


class Spider(object):

    def __init__(self):
        self.offsetSize = Offsetsize()
        self.mysqlClient = MysqlClient()
        self.log = Log("spider.log")

    def insert_data(self, data):
        for info in data:
            user = (info["name"],
                    info["indices"]["num_pubs"],
                    info["indices"]["num_citation"],
                    info["indices"]["h_index"],
                    info["indices"]["g_index"],
                    info["indices"]["sociability"],
                    info["indices"]["diversity"],
                    info["indices"]["activity"])

            user_id = self.mysqlClient.insert_user(user)
            if user_id != -1:
                for tag in info["tags"]:
                    interest = (tag["t"],)
                    interest_id = self.mysqlClient.insert_interest(interest)

                    if interest_id != -1:
                        user_interest = (user_id, interest_id, tag["w"])
                        self.mysqlClient.insert_user_interest(user_interest)


    def crawler_web(self):
        while True:
            try:
                offset, size = self.offsetSize.concurrent_control_get_offset_size()
                if offset == 0 and size == 0:
                    break
                else:
                    try:
                        url = "https://api.aminer.cn/api/leaderboard/person/list/h_index/offset/{offset}/size/{size}".format(offset=offset, size=size)
                        response = requests.get(url)
                        self.insert_data(response.json()["data"])
                        self.log.info("{url} 爬取成功".format(url=url))
                    except Exception as e:
                        self.log.error("{url} 爬取失败".format(url=url))
            except Exception as e:
                self.log.error("redis连接超时")
                break

        self.mysqlClient.close()