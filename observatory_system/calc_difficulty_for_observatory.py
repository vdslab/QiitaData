import json
import glob
import gc
from observatory import observatory
from calc_tags_difficulty import calc_tags_difficulty
from set_best_permutation import set_best_permutation

data_list = []
tags_word_dict = {}
cluster_data = json.load(open("./clustering_sample_data_300.json"))
print(cluster_data["cluster1"])
all_word_data = json.load(open("./word_data/all_words.json"))

for cluster_tags in cluster_data.values():
  for tag in cluster_tags:
    tag_data = json.load(open("../zemi_data/honban_data/" + tag.lower() + "_data.json")) if tag[0] == "." else json.load(open("../zemi_data/honban_data/" + tag[1:].lower() + "_data.json"))
    tags_word_dict[tag] = tag_data["words"]

# 観点語(今回は調べたい領域とする)
perspective_word = "フロントエンド"

# それぞれのタグの、記事データに登場した固有名詞を管理する
tags_words_data = {}

# 特徴語集合を構成する
topic_words_data = observatory(perspective_word, data_list, tags_words_data)

tags_difficulty = calc_tags_difficulty(topic_words_data, tags_words_data)
best_permutation = set_best_permutation(topic_words_data, tags_word_dict, tag_list)
tag_list = []
for tag_data in best_permutation:
    tag_list.append(tag_data["tag"])

print(tag_list)
with open("test.json", mode="wt", encoding="utf-8") as file:
    json.dump(best_permutation, file, ensure_ascii=False, indent=2)
