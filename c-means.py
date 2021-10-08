from skfuzzy.cluster import cmeans
import numpy as np
import json

json_open = open("./tag_words_count.json", "r")
all_text_data = json.load(json_open)
text_data = [] #被りなしの出現単語の配列
words = []

#出現単語の配列を作成する
for i in all_text_data:
    words.append(i["tag"])
    for j in i["words"]:
        tempword = ""
        tempword += j
        if not tempword in text_data:
            text_data.append(tempword)

wordVec = []

for i in all_text_data:
    tempVec = []
    for j in text_data:
        if j in i["words"]:
            tempVec.append(1)
        else:
            tempVec.append(0)
    wordVec.append(tempVec)

data = np.array(wordVec)
cm_result = cmeans(data.T, 3, 1.7, 0.003, 10000)

x = 0.33
BIGCNT = 0
for i in cm_result[1]:
    cnt = 0
    BIGCNT += 1
    print(str(BIGCNT)+":",end="")
    for j in i:
        cnt += 1
        if j > x:
            print(words[cnt-1]+" ", end ="")
#print(cm_result[1])