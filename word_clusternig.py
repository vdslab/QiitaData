from matplotlib import pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import json

json_open = open("./tag_words_count.json", "r")
all_text_data = json.load(json_open)
text_data = []

#一つの単語に出現する単語を半角スペース区切りでまとめる
for i in all_text_data:
    tempword = ""
    for j in i["words"]:
        tempword += ((" "+j)*(i["words"][j]))
    text_data.append(tempword)

#Tf-idfでベクトル化する
vectorizer = TfidfVectorizer(use_idf=True, token_pattern=u'(?u)\\b\\w+\\b')
vecs = vectorizer.fit_transform(text_data)
v = vecs.toarray()

#クラスタリング
cls = KMeans(n_clusters=4)
result = cls.fit(v)

plt.scatter(v[:,0],v[:,1], c=result.labels_)
plt.scatter(result.cluster_centers_[:,0],result.cluster_centers_[:,1],s=250, marker='*',c='red')
plt.show()