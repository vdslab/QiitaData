import csv

f = open('./tags_count_top100.csv') #パスはうまいことしてくれ
dateReader = csv.reader(f)

N = 100 #データの数
resultDate = [["Source","Target","Weight","Type"]] #ヘッダーを先に作っとく
tempDate = [0,0,0,"Undirected"]
next(dateReader) #先頭のデータの名前はいらないのでスキップする

for i in range(N):
    row = next(dateReader)
    for j in range(len(row)):
        if i < j:
            tempDate = [i+1,j+1,int(row[j]),"Undirected"]
            resultDate.append(tempDate)

f.close()

with open('edge.csv', 'w', newline = '') as edge_file: #CSV出力
    writer = csv.writer(edge_file)
    for i in range(len(resultDate)):
        writer.writerow(resultDate[i])