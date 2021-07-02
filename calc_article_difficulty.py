import MeCab
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import json
import numpy as np
import glob
import gc

files = glob.glob("./article_data/*")
print(files)
difficulty_list = []
N = int(input("特徴語をいくつにするか："))
mecab = MeCab.Tagger('-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd')

mecab.parse('')  # 文字列がGCされるのを防ぐ

POS = ["動詞", "名詞", "形容詞", "形容動詞"]
proprietary_noun_page_cnt = {}

def calc_tfidf(word_list, corpus, value):

    global N

    vectorizer = TfidfVectorizer(vocabulary=word_list)
    
    tfidf_result = vectorizer.fit_transform(corpus).toarray()

    del vectorizer
    gc.collect()
    
    tfidf_result = np.max(tfidf_result, axis=0)
    word_tfidf_data = []
    
    for i in range(len(word_list)):
        word_tfidf_data.append([word_list[i], tfidf_result[i]])
    
    del tfidf_result, word_list
    gc.collect()

    sorted_tfidf_result = sorted(word_tfidf_data, key=lambda x: x[1], reverse=True)

    del word_tfidf_data
    gc.collect()
    
    set_tfidf(sorted_tfidf_result[:N], value)


def set_tfidf(sorted_tfids_result, value):

    value["tf-idf"] = {}
    for values in sorted_tfids_result:
        value["tf-idf"][values[0]] = values[1]
        

def count_words(text, word_list, page_cnt):

    while text:
        # 単語を取得
        word = text.surface
        # 品詞を取得
        pos = text.feature.split(",")[0]
        
        # 単語かどうかの判定
        if pos in POS:

            # 固有名詞かどうかの判定
            if text.feature.split(",")[1] == "固有名詞":
                
                # 辞書にキーがあるかどうかの判定
                if word not in word_list:
                    word_list.append(word)

                    if word not in page_cnt.keys():
                        page_cnt[word] = 0
                    page_cnt[word] += 1

        text = text.next


def calc_article_difficulty(data, page_cnt, all_page_cnt):

    global N

    diff = 0

    for key in data["tf-idf"].keys():
        diff += (all_page_cnt - page_cnt[key]) / all_page_cnt

    return diff / min(N, len(data["tf-idf"].keys()))

cnt = 1
for file in files:
    json_open = open(file, "r")
    json_data = json.load(json_open)
    del json_open
    for value in json_data:
        proprietary_noun_dic = {}
        
        for i in range(len(value["body"])):
            value["body"][i] = value["body"][i].replace("\n", "")

        corpus = value["body"]
        word_list = []

        for text in corpus:
            count_words(mecab.parseToNode(text), word_list, proprietary_noun_page_cnt)

        calc_tfidf(word_list, corpus, value)
        del word_list
        gc.collect()


        with open(file, mode="wt", encoding="utf-8") as f:
            json.dump(json_data, f, ensure_ascii=False, indent=2)


        print(str(cnt) + "/" + str(len(files)))
        cnt += 1

for file in files:
    json_open = open(file, "r")
    json_data = json.load(json_open)
    del json_open
    for value in json_data:
        difficulty_list.append({
            "tag": value["tag"],
            "difficulty": calc_article_difficulty(value, proprietary_noun_page_cnt, len(files)),
            "url": "https://qiita.com/tags/" + value["tag"].lower()
        })

with open("difficulty_data.json", mode="wt", encoding="utf-8") as file:
    json.dump(difficulty_list, file, ensure_ascii=False, indent=2)
