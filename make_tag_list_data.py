import json
import glob

tag_data = []

files = glob.glob("./clustering_data/*.json")
print(files)
for file in files:
  file_data = json.load(open(file))
  
  push_data = []
  for data in file_data:
    push_data.append(data["tag"])
  
  tag_data.append(push_data)

with open("./clustering_data/tag_list_data.json", mode = "wt", encoding = "utf-8") as file:
  json.dump(tag_data, file, ensure_ascii = False, indent = 2)