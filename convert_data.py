import json
import glob
    
class UnionFind :
    parent = []
  
    def __init__(self, n): 
      self.parent = []
      for i in range(n): 
        self.parent.append(i)
    
  
    def root(self, x):
      if(self.parent[x] == x):
           return x
      self.parent[x] = self.root(self.parent[x])
      return self.parent[x]
    
  
    def unite(self, x, y): 
      rx = self.root(x)
      ry = self.root(y)
      if(rx == ry):
          return 0
      self.parent[rx] = ry
    
  
    def same(self, x, y):
      rx = self.root(x)
      ry = self.root(y)
  
      if(rx == ry):
        return True
      else:
        return False

def main():
    files = glob.glob("./cluster_diff_sample_data/*.json")
    print(files)
    for file in files:
      print(file)
      res = []
      f1 = open('./jaccard_data_400.json' ,'r', encoding="utf-8_sig")
      f2 = open(file,'r', encoding="utf-8_sig")
      jaccard_data = json.load(f1)
      diff_data = json.load(f2)
      f1.close()
      f2.close()
    
      leng = len(diff_data)

      es = []
      uf = UnionFind(leng)
      print(uf.parent)

      for i in range(leng):
        #print(diff_data[i])
        obj = {}
        obj['nodeName'] = diff_data[i]['tag']
        obj['diff'] = diff_data[i]['difficulty']
        obj['ID'] = i+1
        obj['url'] = 'https://qiita.com/tags/{}'.format(obj['nodeName'].lower()) if diff_data[i]["tag"][0] != "#" else 'https://qiita.com/tags/{}'.format("%23" + obj['nodeName'][1:].lower())
        obj['childNode'] = []
        res.append(obj)
        #print(obj["nodeName"])
      
      #print(res)

      for i in range(leng):
          for j in range(leng):
              if(i != j): 
                  obj = {}
                  obj['From'] = i
                  obj['To'] = j
                  obj['cost'] = jaccard_data[i]['jaccard'][j]
                  es.append(obj)
               
      es = sorted(es, key = lambda x:x['cost'], reverse=True)
      #print(es)
      for item in es:
        if(uf.same(item['To'], item['From']) == False):
              uf.unite(item['To'], item['From'])
              To = -1 
              From = -1
              if(diff_data[item['To']]['difficulty'] >= diff_data[item['From']]['difficulty']):
                  To = item['To']
                  From = item['From']
              else:
                  To = item['From']
                  From = item['To']
              res[From]['childNode'].append(To+1)
      
      #print(res)
      #print(uf.parent)
      with open("./cluster_diff_sample_data/graph_data/" + file.split("/")[2].split("_")[0] + "_graph_data.json", mode = "wt", encoding = "utf-8") as file:
        json.dump(res, file, ensure_ascii = False, indent = 2)

if __name__ == '__main__':
    main()
