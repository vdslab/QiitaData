from skfuzzy.cluster import cmeans
import numpy as np
import json

json_open = open("./all_article_word_data.json", "r")
all_words_data = json.load(json_open)
text_data = [] #被りなしの出現単語の配列
tags = []

#配列lと単語xを入れると、その単語が入っている位置を返す。存在しない単語の場合は-1を返す
def my_index(l, x, default=-1):
    if x in l:
        return l.index(x)
    else:
        return default

#出現単語が重複なしで全て入った配列を作成する
for i in all_words_data:
    #使用するタグだけを入れた配列tagsを作成
    tags.append(i["tag"])
    for j in i["words"]:
        text_data.append(j)

#重複なしかつ順番を統一したいので一旦ソートする
list(set(text_data)).sort()

'''
ここまでの処理は時間的な問題なしなことがチェック済み
'''
vecLen = len(text_data)
print(vecLen)
wordVec = [] #全てのベクトルを入れる配列。最終的には二次元配列になる。

#各タグに対してのベクトルを生成
#それぞれの単語が出現したら1,そうでなければ0を入れたい
#ざっくり10^5~6くらいの数なので処理が遅い
for i in all_words_data:
    tempVec = [0] * vecLen #今からベクトル化したいタグの配列を初期値0で作成
    for j in i["words"]: 
        '''
        タグごとに出現している単語の並び順は実際の文章内での出現順なので、それぞれのタグ間で順番が違うため総単語の並び順をベースに調べるしかないと思ってる。
        総単語数が2929069なので、計算量の工夫が必要そう。この部分での処理が重そうなのは特定済み。
        多分自前の関数のmy_indexが重いんだけど、総単語のリストから位置を特定してベクトルの配列のその位置と同じ位置に1を突っ込む方法以外にパッと思いつかない
        '''
        pos = my_index(text_data,j) #多分ここが重い？
        if pos != -1:
            tempVec[pos] = 1
    wordVec.append(tempVec)
#print(wordVec)

'''
#クラスタリングの処理
data = np.array(wordVec)
cm_result = cmeans(data.T, 3, 1.7, 0.003, 10000)

x = 0.33
BIGCNT = 0
for i in cm_result[1]:
    cnt = 0
    BIGCNT += 1
    print(str(BIGCNT)+":",end="")
    for j in i:
        cnt += 1
        if j > x:
            print(tags[cnt-1]+" ", end ="")
#print(cm_result[1])
'''