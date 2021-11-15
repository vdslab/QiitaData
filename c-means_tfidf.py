from sklearn.feature_extraction.text import TfidfVectorizer
from skfuzzy.cluster import cmeans
import json
import pandas as pd
import numpy as np

def calc_tfidf():
  json_open = open("./all_tag_words_dict.json", "r")
  json_data = json.load(json_open)
  tag_word_list = []
  new_data = []
  cnt = 0
  for data in json_data:
    word_list = []
    for word, count in data["words"].items():
      for i in range(count):
        word_list.append(word)
    
    tag_word_list.append(" ".join(word_list))
    cnt += 1
    print(str(cnt) + "/" + "100")
  

  vectorizer = TfidfVectorizer()
  tfidf_result = vectorizer.fit_transform(word_list)
  
  tfidf_result = tfidf_result.toarray().tolist()
  new_data.append(calc_tfidf(tag_word_list))

  print("TF-IDFのベクトル生成終了")
  return tfidf_result


json_open1 = open("./all_tag_words_dict.json", "r")
json_open2 = open("./all_words.json", "r")
all_words_data = json.load(json_open1)
text_data      = json.load(json_open2)
tags = []

for i in all_words_data:
    tags.append(i["tag"])

wordVec = calc_tfidf()

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
print(cm_result[1])