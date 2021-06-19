import json
from bs4 import BeautifulSoup
import re

json_open = open("react_article_data.json", "r")
json_data = json.load(json_open)

for value in json_data.values():
    # URLだけの記事によるエラーを避けるためにURL削除
    text = re.sub("(https?|ftp)(:\/\/[-_\.!~*\'()a-zA-Z0-9;\/?:\@&=\+$,%#]+)", "", value["body"])

    #削除した記事を読み込む
    text = BeautifulSoup(text, "html.parser")
    
    #<code>タグが含まれない記事の場合スルーする
    if text.find("code") == None:
        continue

    text.find("code").extract()
    value["body"] = str(text)

with open("react_article_data.json", mode = "wt", encoding = "utf-8") as file:
    json.dump(json_data, file, ensure_ascii = False, indent = 2)