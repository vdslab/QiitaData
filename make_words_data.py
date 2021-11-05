import MeCab
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import json
import numpy as np
import glob

tags = json.load(open("./all_tags_data.json"))
tags = list(tags.keys())[:100]
print(tags)
difficulty_list = []
mecab = MeCab.Tagger('-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd')

mecab.parse('')  # 文字列がGCされるのを防ぐ

POS = ["動詞", "名詞", "形容詞", "形容動詞"]
proprietary_noun_page_cnt = {}

def count_words(text, word_dict, page_cnt, tags):

    global words_cnt
    while text:
        # 単語を取得
        word = text.surface
        # 品詞を取得
        pos = text.feature.split(",")[0]
        
        # 単語かどうかの判定
        if pos in POS:

            # 固有名詞かどうかの判定
            if text.feature.split(",")[1] == "固有名詞":
                # 固有名詞が延何回出現したかカウントする
                words_cnt += 1

                # 抽出する固有名詞を対象のタグ名のみに絞る
                if word in tags:
                
                    # 辞書にキーがあるかどうかの判定
                    if word not in word_dict:
                        word_dict[word] = 0
                
                    word_dict[word] += 1

        text = text.next

all_word_data = []
cnt = 1
for tag in tags:
    json_data = json.load(open("./words_data/" + tag.lower() + "_data.json", "r"))
    
    for value in json_data:
        proprietary_noun_dic = {}
        
        for i in range(len(value["body"])):
            value["body"][i] = value["body"][i].replace("\n", "")

        corpus = value["body"]
        word_dict = {}
        words_cnt = 0

        for text in corpus:
            count_words(mecab.parseToNode(text), word_dict, proprietary_noun_page_cnt,tags)

        word_data = [{
            "tag": value["tag"],
            "words": word_dict

        }]
        all_word_data.append({
            "tag": value["tag"],
            "words": word_dict,
            "words_count": words_cnt
        })

        print(str(cnt) + "/" + str(len(tags)))
        cnt += 1

with open("./all_tags_word.json", mode="wt", encoding="utf-8") as f:
    json.dump(all_word_data, f, ensure_ascii=False, indent=2)
    