import json
from math import ceil

jaccard_data = json.load(open("./jaccard_data_300.json"))
tag_data = []
for data in jaccard_data:
  tag_data.append(data["tag"])

new_jaccard_data = {}
for data in jaccard_data:
  new_jaccard_data[data["tag"]] = {}
  for i in range(len(data["jaccard"])):
    new_jaccard_data[data["tag"]][tag_data[i]] = data["jaccard"][i]
  
for i in range(1, 5):
  cluster_data = json.load(open("../Qiitaviz2021/public/data/system2/cluster" + str(i) + "_graph_data.json"))

  cluster_id_dict = {}
  group_count = ceil(len(cluster_data) / 5)
  for data in cluster_data:
    cluster_id_dict[data["ID"]] = data["nodeName"]

  create_data = []
  for data in cluster_data:
    for child_node in data["childNode"]:
      append_data = {}
      append_data["source"] = data["nodeName"]
      append_data["target"] = cluster_id_dict[child_node]
      append_data["jaccard"] = new_jaccard_data[data["nodeName"]][cluster_id_dict[child_node]]
      create_data.append(append_data)
  
  sorted_data = sorted(create_data, key=lambda x:x['jaccard'], reverse=True)

  group_num = 1
  cnt = 0
  for data in sorted_data:
    data["edgeGroup"] = group_num
    cnt += 1
    if cnt % group_count == 0:
      group_num -= 0.2
  output_data = []

  append_data = {}
  for data in sorted_data:
    if data["source"] not in append_data.keys():
      append_data[data["source"]] = {}
    append_data[data["source"]][data["target"]] = data["edgeGroup"]
  output_data.append(append_data)
  
  with open("./jaccard_data/system2/cluster" + str(i) + "_edge_data.json", mode = "wt", encoding = "utf-8") as file:
    json.dump(output_data, file, ensure_ascii = False, indent = 2)
