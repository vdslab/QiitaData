from skfuzzy.cluster import cmeans
import numpy as np
import json

json_open1 = open("./all_tag_words_dict.json", "r")
json_open2 = open("./all_words.json", "r")
all_words_data = json.load(json_open1)
text_data      = json.load(json_open2)
tags = []

'''
for i in all_words_data:
    #使用するタグだけを入れた配列tagsを作成
    tags.append(i["tag"])
    for j in i["words"]:
        text_data.append(j)
'''

allWordCnt = len(text_data["words"])
zero_allay = [0]*allWordCnt
wordVec = [] #全てのベクトルを入れる配列。最終的には二次元配列になる。

#各タグに対してのベクトルを生成
#それぞれの単語が出現したら1,そうでなければ0を入れたい
n = 1000 #上位n件の値

for i in all_words_data:
    tempVec = dict(zip(text_data["words"],zero_allay))#今からベクトル化したいタグの辞書を作成
    appearanceWordList = dict(zip(i["words"],zero_allay)) #出現単語の辞書型valueは初期値0で作成
    tags.append(i["tag"])
    for j in range(n): 
        word = text_data["words"][j]
        if word in appearanceWordList:
            tempVec[word] = 1
    wordVec.append(list(tempVec.values()))
#クラスタリングの処理
data = np.array(wordVec)
cm_result = cmeans(data.T, 5, 1.3, 0.003, 10000)

x = 0.25 #この値を超えたもののみ採用する
BIGCNT = 0

#cm_result[1]に結果が入ってる

for i in cm_result[1]:
    BIGCNT += 1
    cnt = 0
    print(str(BIGCNT)+":",end="")
    for j in i:
        cnt += 1
        if j > x:
            print(tags[cnt-1]+" ", end ="")
    print("")