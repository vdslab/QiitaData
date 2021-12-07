import json
from math import ceil

for i in range(1, 5):
  json_data = json.load(open("../Qiitaviz2021/public/data/system2/cluster" + str(i) + "_graph_data.json"))
  group_count = ceil(len(json_data) / 5)

  sorted_data = sorted(json_data, key=lambda x:x['diff'])
  group_num = 0
  cnt = 0
  for data in sorted_data:
    data["color_group"] = group_num
    cnt += 1
    if cnt % group_count == 0:
      group_num += 1
  
  with open("./cluster_diff_sample_data/graph_data/cluster" + str(i) + "_graph_data.json", mode = "wt", encoding = "utf-8") as file:
    json.dump(sorted_data, file, ensure_ascii = False, indent = 2)
