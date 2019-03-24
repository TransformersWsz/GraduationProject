import requests
from requests.exceptions import ConnectionError
from bs4 import BeautifulSoup

base_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7'
}

def get_page(url, options={}):
    """
    抓取代理
    :param url: 代理地址
    :param options:
    :return: 抓取结果
    """
    headers = dict(base_headers, **options)
    print('正在抓取{url}'.format(url=url))
    try:
        response = requests.get(url, headers=headers)
        print('抓取成功', url, response.status_code)
        if response.status_code == 200:
            return response.text.encode(response.encoding)
    except ConnectionError:
        print('抓取{url}失败'.format(url=url))
        return None


def parse(html_doc):
    soup = BeautifulSoup(html_doc, "html.parser")
    table = soup.find_all("table")[-1]
    trs = table.find_all("tr")
    proxies = []
    for tr in trs:
        if tr.td.string != "ip":
            proxies.append(":".join([tr.td.string, tr.td.next_sibling.string]))
    return proxies


if __name__ == "__main__":
    print(__name__)
    html_doc = get_page("http://www.66ip.cn/1.html")
    proxies = parse(html_doc)
    print(proxies)
