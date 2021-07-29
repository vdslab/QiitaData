import json
import glob
import copy
files = glob.glob("./clustering_data/graph_data/*.json")
print(files)

def dfs(data, i, count):
  max_count = 0
  if len(data[i]["childNode"]) == 0:
    data[i]["level"] = count
    return count
  
  for child in data[i]["childNode"]:
    max_count = max(max_count, dfs(data, child - 1, count + 1))
    data[i]["level"] = count

  return max_count

def set_level(json_data, parent_flag, root_flag, level, i):
  if root_flag[i] == 1:
    return 

  root_flag[i] = 1
  json_data[i]["level"] =  level#max(level, json_data[i]["level"])
  for child in json_data[i]["childNode"]:
    set_level(json_data, parent_flag, root_flag, level + 1, child - 1)
  
  for parent in parent_flag[i]:
    set_level(json_data, parent_flag, root_flag, level - 1, parent - 1)

  return json_data

for file in files:

  json_data = json.load(open(file))
  n = len(json_data)
  parent_flag = [[] for _ in range(n)]

  # 持っている親を格納する
  for data in json_data:
    for child in data["childNode"]:
      parent_flag[child - 1].append(data["ID"])
  max_count = 0
  
  for i in range(n):
    if len(parent_flag[i]):
      continue
    data = copy.deepcopy(json_data)
    root_flag = [0] * n
    count = dfs(data, i, 0)

    if max_count <= count:
      json_data = set_level(json_data, parent_flag, root_flag, 0, i)
      max_count = count

  with open("./clustering_data/graph_data/" + file.split("/")[3].split("_")[0] + "_graph_data.json", mode = "wt", encoding = "utf-8") as file:
    json.dump(json_data, file, ensure_ascii = False, indent = 2)