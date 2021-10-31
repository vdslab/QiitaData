import json

json_open = open("./all_article_word_data.json", "r")
all_words_data = json.load(json_open)
text_data = [] #被りなしの出現単語の配列
tags = []

#出現単語が重複なしで全て入った配列を作成する
for i in all_words_data:
    #使用するタグだけを入れた配列tagsを作成
    tags.append(i["tag"])
    for j in i["words"]:
        text_data.append(j)

#重複なしかつ順番を統一したいので一旦ソートする
text_data = sorted(list(set(text_data)))

json_data = {"words":text_data}

j_w = open("./all_words.json","w")
json.dump(json_data,j_w,indent=2,ensure_ascii=False)
j_w.close()