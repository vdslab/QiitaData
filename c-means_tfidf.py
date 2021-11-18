from sklearn.feature_extraction.text import TfidfVectorizer
from skfuzzy.cluster import cmeans
import json
import pandas as pd
import numpy as np

def set_tfidf_data(tags):
  N = 2
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


tags = []
all_words_data = set_tfidf_data(tags)
#print(len(all_words_data[0]))

wordVec = calc_tfidf(all_words_data)
#クラスタリングの処理
k = 4
m = 1.1

with open('datasize200_cluster4.txt','w') as f:
  while m < 1.3:
    cm_result = cmeans(wordVec.T, k, m, 0.003, 10000)

    x =  1/k #この値を超えたもののみ採用する
    BIGCNT = 0

    #cm_result[1]に結果が入ってる
    print("m = "+str(m),file=f)
    for i in cm_result[1]:
        BIGCNT += 1
        cnt = 0
        print("cluster"+str(BIGCNT)+":",end="",file=f)
        for j in i:
            cnt += 1
            if j > x:
                print(tags[cnt-1]+" ", end ="",file=f)
        print("",file=f)
    m += 0.05