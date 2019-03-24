from .utils import get_page
from bs4 import BeautifulSoup

class ProxyMetaclass(type):
    def __new__(cls, name, bases, attrs):
        count = 0
        attrs["__CrawlFunc__"] = []
        for k, v in attrs.items():
            if "crawl_" in k:
                attrs["__CrawlFunc__"].append(k)
                count += 1
        attrs["__CrawlFuncCount__"] = count
        return type.__new__(cls, name, bases, attrs)


class Crawler(object, metaclass=ProxyMetaclass):
    def get_proxies(self, callback):
        proxies = []
        for proxy in eval("self.{}()".format(callback)):
            proxies.append(proxy)
        return proxies

    def crawl_daili66(self, page_count=5):
        """
        爬取代理
        :param page_count: 爬取页数
        :return: ip:port
        """
        base_url = "http://www.66ip.cn/{page}.html"
        urls = [base_url.format(page=page) for page in range(1, page_count + 1)]
        for url in urls:
            html_doc = get_page(url)
            if html_doc != None:
                soup = BeautifulSoup(html_doc, "html.parser")
                table = soup.find_all("table")[-1]
                trs = table.find_all("tr")
                for tr in trs:
                    if tr.td.string != "ip":
                        ip = tr.td.string
                        port = tr.td.next_sibling.string
                        yield ":".join([ip, port])
