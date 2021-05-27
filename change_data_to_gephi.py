import json
import csv

json_open = open('tags_count_data_top100.json', 'r') #(直下にある使いたいファイル名,r)で読み込み
load_data = json.load(json_open)


N = 100
keyList = list(load_data.keys())
dataTypeList = ["total","jaccard","simpson"]
resultData = [["Source","Target","Weight","Type"]] #ヘッダーを先に作っとく

print("出力したいデータのタイプを以下の数字から選んでください。\n0:total\n1:jaccard\n2:simpson")
dataType = int(input())

if dataType < 0 or dataType > 2:
    exit()

for i in range(N):
    for j in range(N):
        if i < j:
            resultData.append([i+1,j+1,load_data[keyList[i]][keyList[j]][dataTypeList[dataType]],"Undirected"])

fileName = "edge_"+dataTypeList[dataType]+".csv"
with open(fileName, 'w', newline = '') as edge_file: #CSV出力
    writer = csv.writer(edge_file)
    for i in range(len(resultData)):
        writer.writerow(resultData[i])