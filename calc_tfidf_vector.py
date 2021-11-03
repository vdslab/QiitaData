from sklearn.feature_extraction.text import TfidfVectorizer
import json
import pandas as pd
import numpy as np

def calc_tfidf():
  """
  指定しているタグの固有名詞についてTF-IDFを算出し、そのベクトルを返す関数
  Returns
  -------
  result : TF-IDFのベクトルが格納されたlist
  """
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