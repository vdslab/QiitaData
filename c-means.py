# -*- coding: utf-8 -*-
from skfuzzy.cluster import cmeans
import numpy as np
import json

json_open0 = open("./all_words.json", "r")
json_open1 = open("./tag_words_count_data/tag_words_count_data_1_100.json", "r")
json_open2 = open("./tag_words_count_data/tag_words_count_data_101_200.json", "r")
json_open3 = open("./tag_words_count_data/tag_words_count_data_201_300.json", "r")
json_open4 = open("./tag_words_count_data/tag_words_count_data_301_400.json", "r")
json_open5 = open("./tag_words_count_data/tag_words_count_data_401_500.json", "r")


text_data      = json.load(json_open0)
data1  =  json.load(json_open1)
data2  =  json.load(json_open2)
data3  =  json.load(json_open3)
#data4  =  json.load(json_open4)
#data5  =  json.load(json_open5)
#all_words_data = [data1,data2,data3,data4,data5]
all_words_data = [data1,data2,data3]

tags = []


allWordCnt = len(text_data["words"])
zero_array = [0]*allWordCnt
wordVec = [] #全てのベクトルを入れる配列。最終的には二次元配列になる。

#各タグに対してのベクトルを生成
#それぞれの単語が出現したら1,そうでなければ0を入れたい

n = 1000 #上位n件の値



for i in all_words_data:
    for j in i:
        tempVec = dict(zip(text_data["words"],zero_array))#今からベクトル化したいタグの辞書を作成
        appearanceWordList = dict(zip(j["words"],zero_array)) #出現単語の辞書型valueは初期値0で作成
        tags.append(j["tag"])
        for k in range(n): 
            word = text_data["words"][k]
            if word in appearanceWordList:
                tempVec[word] = 1
        wordVec.append(list(tempVec.values()))

#クラスタリングの処理
data = np.array(wordVec)
#cmeans(いじるな,クラスタ数(整数),m値(1以上の実数で小さい程厳密に分けてくれる),いじるな,いじるな)
#クラスタ数とm値を変えて頑張る
#m値は1.2以下だと少数がめちゃくちゃ長くなるので、これ以上の値がおすすめ。1.5以上だと全部同じ値になるから、1.2〜1.5の範囲がいいかも
cm_result = cmeans(data.T, 4, 1.3, 0.003, 10000)

x = 0.35 #この値を超えたもののみ採用する
#xの値は1/クラスタ数 以上の値でいい感じに
BIGCNT = 0
create_data = {}
#cm_result[1]に結果が入ってる
for i in cm_result[1]:
    BIGCNT += 1
    cnt = 0
    data = []
    #print(str(BIGCNT)+":",end="")
    for j in i:
        cnt += 1
        if j > x:
            #print(tags[cnt-1]+" ", end ="")
            data.append(tags[cnt - 1])
    create_data["cluster" + str(BIGCNT)] = data
    #print("")

with open("clustering_sample_data_300.json", mode = "wt", encoding = "utf-8") as file:
    json.dump(create_data, file, ensure_ascii = False, indent = 2)