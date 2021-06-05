# ライブラリのインポート
import http.client
import pandas as pd
import json
import os

# 取得したいページ数
TOTAL_PAGE = 1
TIME = TOTAL_PAGE
PER_PAGE = 100
TOKEN = os.environ["QIITA_TOKEN"]
# ユーザ認証
h = {'Authorization': 'Bearer {}'.format(TOKEN)}
connect = http.client.HTTPSConnection("qiita.com")
url1 = "/api/v2/tags?"
url2 ="&sort=count"

# カウント変数
num = 0
pg = 0
count = 1
data_dict = dict()

# データを取得してtxtファイルに900個記事を書き出す
for count in range(1, 101):
    page = "page=" + str(count) + "&per_page=" + str(PER_PAGE)
    connect.request("GET", url1 + page + url2, headers=h)
    res = connect.getresponse()
    data = res.read().decode("utf-8")
    new_data = json.loads(data)
    print(count)
    for i in range(len(new_data)):
        data_dict[new_data[i]["id"]] = {}
        data_dict[new_data[i]["id"]]["items_count"] = new_data[i]["items_count"]
        data_dict[new_data[i]["id"]]["followers_count"] = new_data[i]["followers_count"]
        
with open('all_tags_data.json', mode = 'wt') as file:
    json.dump(data_dict, file, ensure_ascii = False, indent = 2)