import json

json_data = json.load(open("./clustering_sample_data_300.json"))
create_data = []
cnt = 1
for cluster in json_data.values():
  print("### cluster" + str(cnt) + " " + str(len(cluster)) + "個")
  print(cluster)
  create_data.append(cluster)
  cnt += 1
"""
with open("tag_list_data.json", mode = "wt", encoding = "utf-8") as file:
    json.dump(create_data, file, ensure_ascii = False, indent = 2)
"""