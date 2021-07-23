import MeCab
import pandas as pd
import json
import numpy as np

json_open = open("react_article_data.json", "r")
json_data = json.load(json_open)
mecab = MeCab.Tagger ('-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd')
while !epe

mecab.parse('')#文字列がGCされるのを防ぐ
POS = ["動詞", "名詞", "形容詞", "形容動詞"]
proprietary_noun_page_cnt = {}

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

for value in json_data.values():
    proprietary_noun_dic = {}
    count_words(mecab.parseToNode(value["body"]), proprietary_noun_dic, proprietary_noun_page_cnt)

    corpus = value["body"].replace(".", "。").replace("\n", "").split("。")
    word_list = list(proprietary_noun_dic.keys())
    print(word_list)