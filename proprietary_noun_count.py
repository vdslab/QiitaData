import MeCab
import json

json_open = open("react_article_data_sample.json", "r")
json_load = json.load(json_open)

mecab = MeCab.Tagger ('-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd')

mecab.parse('')#文字列がGCされるのを防ぐ
hinshi = ["動詞", "名詞", "形容詞", "形容動詞"]
proprietary_noun_dic = {}
word_total_count = 0
def count_words(text, cnt, dic):
    while text:

        #単語を取得
        word = text.surface
        #品詞を取得
        pos = text.feature.split(",")[0]
        # 単語かどうかの判定
        if pos == "動詞" or pos == "名詞" or pos == "形容詞" or pos == "形容動詞":
            cnt += 1

            # 固有名詞かどうかの判定
            if text.feature.split(",")[1] == "固有名詞":
                #print(word, text.feature.split(",")[1])
                # 辞書にキーがあるかどうかの判定
                if word not in dic.keys():
                    dic[word] = 0

                dic[word] += 1
        text = text.next

cnt = 0
for key, item in json_load.items():
    cnt += 1
    if cnt < 5:
        continue
    count_words(mecab.parseToNode(key), word_total_count, proprietary_noun_dic)
    count_words(mecab.parseToNode(item["body"]), word_total_count, proprietary_noun_dic)
    
    print(item["url"], item["body"])
    if cnt == 8:
        break
print(word_total_count, proprietary_noun_dic)
