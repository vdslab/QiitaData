import json

json_open1 = open("./tag_words_count_data/tag_words_count_data_1_100.json", "r")
json_open2 = open("./tag_words_count_data/tag_words_count_data_101_200.json", "r")
json_open3 = open("./tag_words_count_data/tag_words_count_data_201_300.json", "r")
json_open4 = open("./tag_words_count_data/tag_words_count_data_301_400.json", "r")
json_open5 = open("./tag_words_count_data/tag_words_count_data_401_500.json", "r")
all_words_data1 = json.load(json_open1)
all_words_data2 = json.load(json_open2)
all_words_data3 = json.load(json_open3)
all_words_data4 = json.load(json_open4)
all_words_data5 = json.load(json_open5)
text_data = [] #被りなしの出現単語の配列

#出現単語が重複なしで全て入った配列を作成する
for i in all_words_data1:
    for j in i["words"]:
        text_data.append(j)

for i in all_words_data2:
    for j in i["words"]:
        text_data.append(j)

for i in all_words_data3:
    for j in i["words"]:
        text_data.append(j)

for i in all_words_data4:
    for j in i["words"]:
        text_data.append(j)
        
for i in all_words_data5:
    for j in i["words"]:
        text_data.append(j)

#重複なしかつ順番を統一したいので一旦ソートする
text_data = sorted(list(set(text_data)))

json_data = {"words":text_data}

j_w = open("./all_words.json","w")
json.dump(json_data,j_w,indent=2,ensure_ascii=False)
j_w.close()