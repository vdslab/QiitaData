import json
for i in range(1, 5):
  json_data = json.load(open("./public/data/system2/cluster" + str(i) + "_graph_data.json"))
  parent_array = [[] for _ in range(len(json_data))]
  for data in json_data:
    for child_node in data["childNode"]:
      parent_array[child_node - 1].append(data["ID"])
  for data in json_data:
    data["parentNode"] = parent_array[data["ID"] - 1]
    if data["nodeName"] == "Azure":
      print(data)
  
  with open("./public/data/system2/cluster" + str(i) + "_graph_data.json", mode = "wt", encoding = "utf-8") as file:
    json.dump(json_data, file, ensure_ascii = False, indent = 2)
