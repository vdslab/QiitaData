from sklearn.feature_extraction.text import TfidfVectorizer
from skfuzzy.cluster import cmeans
import json
import pandas as pd
import numpy as np

N = 2
def set_tfidf_data(tags):
  cluster_size = N * 100

  #dtype=str にすると文字数制限がかかっているらしくバグるので注意
  tag_words_list = np.empty(cluster_size, dtype=object)
  
  cnt = 0
  #TF-IDF算出用のデータ生成
  for i in range(1, N * 100, 100):
    tags_data = json.load(open("./tag_words_count_data/tag_words_count_data_" + str(i) + "_" + str(i + 99) + ".json"))
    #print(len(tags_data))
    for tag_data in tags_data:
      words = ""
      tags.append(tag_data["tag"])
      for word, word_count in tag_data["words"].items():
        for i in range(word_count):
          if words != "":
              words += " "
          words += word
                
      tag_words_list[cnt] = words
      cnt += 1
  return tag_words_list
            
def calc_tfidf(words_list):
  vectorizer = TfidfVectorizer()
  tfidf_result = vectorizer.fit_transform(words_list)
  
  tfidf_result = tfidf_result.toarray()

  print("TF-IDFのベクトル生成終了")
  return tfidf_result


json_open = open("./all_words.json", "r")
tags = []
all_words_data = set_tfidf_data(tags)
text_data      = json.load(json_open)

wordVec = calc_tfidf(all_words_data)

#クラスタ数
X = 3
#クラスタリングの処理
data = np.array(wordVec)
cm_result = cmeans(data.T, X, 1.35, 0.003, 10000)

x = 1 / X #この値を超えたもののみ採用する

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
