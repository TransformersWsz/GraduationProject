import requests

proxy = "125.26.99.84:60493"

proxies = {
    "http": "http://" + proxy,
    "https": "https://" + proxy
}

# try:
#     response = requests.get("https://api.aminer.cn/api/leaderboard/person/list/g_index/offset/0/size/20", proxies=proxies)
#     print(response.json())
#     print("----")
# except requests.exceptions.ConnectionError as e:
#     print(e.args)

response = requests.get("https://api.aminer.cn/api/leaderboard/person/list/g_index/offset/0/size/20")
print(response.json())
print("----")