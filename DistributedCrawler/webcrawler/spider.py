import requests

from .log import Log
from .offsetsize import Offsetsize

class Spider(object):
    def __init__(self):
        self.offsetSize = Offsetsize()
        self.log = Log()

    def crawler_web(self):
        while True:
            offset, size = self.offsetSize.concurrent_control_get_offset_size()
            if offset == 0 and size == 0:
                break
            else:
                try:
                    url = "https://api.aminer.cn/api/leaderboard/person/list/g_index/offset/{offset}/size/{size}".format(offset=offset, size=size)
                    response = requests.get(url)
                    self.log.info("{url} 爬取成功".format(url=url))
                except Exception as e:
                    self.log.error("{url} 爬取失败".format(url=url))