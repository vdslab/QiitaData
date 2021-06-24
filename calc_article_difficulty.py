import MeCab
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import json
import numpy as np

json_open = open("react_article_data.json", "r")
json_data = json.load(json_open)
N = int(input("特徴語をいくつにするか："))
mecab = MeCab.Tagger ('-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd')

mecab.parse('')#文字列がGCされるのを防ぐ

POS = ["動詞", "名詞", "形容詞", "形容動詞"]
proprietary_noun_page_cnt = {}

def calc_tfidf(word_list, corpus, value):

    global N

    vectorizer = TfidfVectorizer(vocabulary=word_list)
    tfidf_result = vectorizer.fit_transform(corpus).toarray()
    max_tfidf = np.max(tfidf_result, axis=0)
    word_tfidf_data = []

    for i in range(len(word_list)):
        word_tfidf_data.append([word_list[i], max_tfidf[i]])

    sorted_tfidf_result = sorted(word_tfidf_data, key=lambda x: x[1], reverse=True)

    set_tfidf(sorted_tfidf_result[:N], value)


def set_tfidf(sorted_tfids_result, value):
    
    value["tf-idf"] = {}
    for values in sorted_tfids_result:
        value["tf-idf"][values[0]] = values[1]
    

def count_words(text, dic, page_cnt):

    word_total_count = 0

    while text:

        #単語を取得
        word = text.surface
        #品詞を取得
        pos = text.feature.split(",")[0]
        
        # 単語かどうかの判定
        if pos in POS:
            word_total_count += 1

            # 固有名詞かどうかの判定
            if text.feature.split(",")[1] == "固有名詞":

                # 辞書にキーがあるかどうかの判定
                if word not in dic.keys():
                    dic[word] = 0
                    if word not in page_cnt.keys():
                        page_cnt[word] = 0
                    
                    page_cnt[word] += 1

                dic[word] += 1

        text = text.next

def calc_article_difficulty(data, page_cnt, all_page_cnt):

    global N

    diff = 0

    for key in data["tf-idf"].keys():
        diff += (all_page_cnt - page_cnt[key]) / all_page_cnt

    data["article_difficulty"] = diff / min(N, len(data["tf-idf"].keys()))

for value in json_data:
    corpus = list(set(value["body"].replace(".", "。").replace("\n", "。").split("。")))
    proprietary_noun_dic = {}

    if corpus[0] == "":
        corpus.pop(0)

    count_words(mecab.parseToNode(value["body"]), proprietary_noun_dic, proprietary_noun_page_cnt)

    word_list = list(proprietary_noun_dic.keys())

    if not len(word_list):
        value["tf-idf"] = "undifined"
        continue

    calc_tfidf(word_list, corpus, value)
    
for value in json_data:
    if value["tf-idf"] == "undifined":
        value["article_difficulty"] = "undifined"
        del value["tf-idf"]
        continue

    calc_article_difficulty(value, proprietary_noun_page_cnt, len(json_data))
    del value["tf-idf"]
    del value["body"]

with open("react_article_difficulty_data2.json", mode = "wt", encoding = "utf-8") as file:
    json.dump(json_data, file, ensure_ascii = False, indent = 2)
