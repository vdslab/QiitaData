import MeCab
import json

json_open = open("react_article_data.json", "r")
json_data = json.load(json_open)
N = input("特徴語をいくつにするか：")
mecab = MeCab.Tagger ('-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd')

mecab.parse('')#文字列がGCされるのを防ぐ
POS = ["動詞", "名詞", "形容詞", "形容動詞"]
proprietary_noun_dic = {}
proprietary_noun_page_cnt = {}

def calc_tf_idf(dic, word_cnt, data):
    global N
    for key in dic.keys():
        dic[key] /= word_cnt
    sorted_dic = sorted(dic.items(), key = lambda x:x[1], reverse=True)
    data["tf-idf"] = {}
    i = 0
    for key in sorted_dic:
        if i == 10:
            break
        data["tf-idf"][key[0]] = dic[key[0]]
        i += 1

def count_words(text, dic, page_cnt, data):
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

    calc_tf_idf(dic, word_total_count, data)

def calc_article_difficulty(data, page_cnt, all_page_cnt):
    diff = 0
    for key in data["tf-idf"].keys():
        diff += (all_page_cnt - page_cnt[key]) / all_page_cnt
    data["article_difficulty"] = diff
    print(diff)

for key, value in json_data.items():
    count_words(mecab.parseToNode(key + value["body"]), proprietary_noun_dic, proprietary_noun_page_cnt, value)
    #print(json_data[key])

for value in json_data.values():
    calc_article_difficulty(value, proprietary_noun_page_cnt, len(json_data))
    del value["body"]

with open("react_article_difficulty_data.json", mode = "wt", encoding = "utf-8") as file:
    json.dump(json_data, file, ensure_ascii = False, indent = 2)