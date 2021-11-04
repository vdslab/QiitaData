import json
n = 0
json_data = json.load(open("./difficulty_data_100.json"))
for data in json_data:
  n = max(n, data["group"])

new_file_data = [[] for _ in range(n)]
for data in json_data:
  new_file_data[data["group"] - 1].append(data)

for i in range(n):
  with open("./clustering_data/cluster" + str(i + 1) + "_difficulty_data.json", mode = "wt", encoding = "utf-8") as file:
    json.dump(new_file_data[i], file, ensure_ascii = False, indent = 2)