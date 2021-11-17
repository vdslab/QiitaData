import MeCab
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import json
import numpy as np
import glob
import gc

tags_data = json.load(open("./clustering_sample_data.json"))
difficulty_list = []
#N = int(input("特徴語をいくつにするか："))
N = 10
mecab = MeCab.Tagger('-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd')

mecab.parse('')  # 文字列がGCされるのを防ぐ

POS = ["動詞", "名詞", "形容詞", "形容動詞"]
proprietary_noun_page_cnt = {}

#TF-IDF計算
def calc_tfidf(word_list, data_dic):

    global N

    vectorizer = TfidfVectorizer()
    tfidf_result = vectorizer.fit_transform(word_list).toarray()

    tfidf_label = vectorizer.get_feature_names()
    print("TF-IDF計算終了")
    del vectorizer
    gc.collect()
    
    del word_list
    gc.collect()
    cnt = 0

    for data_value in data_dic.values():
        word_tfidf_data = [["", ""] for _ in range(len(tfidf_label))]
        
        print(cnt)
        for j in range(len(tfidf_label)):
            word_tfidf_data[j][0] = tfidf_label[j]
            word_tfidf_data[j][1] = tfidf_result[cnt][j]

        word_tfidf_data = sorted(word_tfidf_data, key=lambda x: x[1], reverse=True)
        set_tfidf(word_tfidf_data[:N], data_value)
        cnt += 1
    
    del tfidf_result, tfidf_label, word_tfidf_data
    gc.collect()
    print("各タグのTF-IDF上位" + str(N) + "件の単語を算出終了")


def set_tfidf(word_tfidf_data, value):

    for word_data in word_tfidf_data:
        value["tfidf_words"].append(word_data[0])
        

cnt = 0
cluster_num = 1
#クラスタ毎の難易度計算
for tags in tags_data.values():
    #クラスタリング毎のデータ格納用List
    tags_diff_data = []
    cluster_size = len(tags)
    data_dic = {}
    #dtype=str にすると文字数制限がかかっているらしくバグるので注意
    tag_words_list = np.empty(cluster_size, dtype=object)
    
    #TF-IDF算出用のデータ生成
    for i in range(1, 400, 100):
        tags_data = json.load(open("./tag_words_count_data/tag_words_count_data_" + str(i) + "_" + str(i + 99) + ".json"))
            #print(len(tags_data))
        for tag_data in tags_data:
            #読み込んだデータが現在のクラスタに属していなければスルー
            if tag_data["tag"] not in tags:
                continue

            words = ""
            data_dic[tag_data["tag"]] = {
                "tag": tag_data["tag"],
                "tfidf_words":[],
                "diff":0
            }
    
            for word, word_count in tag_data["words"].items():
                for i in range(word_count):
                    if words != "":
                        words += " "
                    words += word
                
            tag_words_list[cnt] = words
            
    del words
    gc.collect()

    #TF-IDF計算
    calc_tfidf(tag_words_list, data_dic)
    
    #ここから難易度計算
    for tag in tags:
        #.から始まるファイルは作成できないのでそのタグの時のみ例外的に処理を加える
        json_open = open("../zemi_data/honban_data/" + tag.lower() + "_data.json", "r") if tag[0] != "." else open("../zemi_data/honban_data/" + tag[1:].lower() + "_data.json", "r")
        json_data = json.load(json_open)
        del json_open
        words_cnt = {}
        for tfidf_word in data_dic[tag]["tfidf_words"]:
            words_cnt[tfidf_word] = 0
        
        for value in json_data:
            for tfidf_word in data_dic[tag]["tfidf_words"]:
                for text in value["body"]:
                    if tfidf_word in text:
                        words_cnt[tfidf_word] += 1

        text_size = len(json_data[0]["body"])
        for tfidf_word in data_dic[tag]["tfidf_words"]:
            data_dic[tag]["diff"] += (text_size - words_cnt[tfidf_word]) / text_size

    create_data = []
    for key, value in data_dic.items():
        create_data.append({
            "tag": value["tag"],
            "difficulty": value["diff"] / N
        })
    
    print("難易度計算終了")
    with open("./cluster_diff_sample_data/cluster" + str(cluster_num) + "_diff.json", mode="wt", encoding="utf-8") as f:
        json.dump(create_data, f, ensure_ascii=False, indent=2)
    cluster_num += 1