import json
    
class UnionFind :
    parent = []
  
    def __init__(self, n): 
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
    res = []
    f1 = open('jaccard_data_100.json' ,'r', encoding="utf-8_sig")
    f2 = open('difficulty_data_100.json','r', encoding="utf-8_sig")
    jaccard_data = json.load(f1)
    diff_data = json.load(f2)
    f1.close()
    f2.close()
    
    leng = len(jaccard_data)

    es = []
    uf = UnionFind(leng)

    for i in range(leng):
        obj = {}
        obj['nodeName'] = diff_data[i]['tag']
        obj['diff'] = diff_data[i]['difficulty']
        obj['ID'] = i+1
        obj['url'] = 'https://qiita.com/tags/{}'.format(obj['nodeName'].lower())
        obj['childNode'] = []
        res.append(obj)
    
    for i in range(leng):
        for j in range(leng):
            if(i != j): 
                obj = {}
                obj['From'] = i
                obj['To'] = j
                obj['cost'] = jaccard_data[i]['jaccard'][j]
                es.append(obj)
               
        
    es = sorted(es, key = lambda x:x['cost'], reverse=True)
    
    #for i in range(20):
    #    print(es[i])

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

    for i in range(20):
      print(res[i])
    
    with open('new_data.json', 'w', encoding='utf-8') as f:
      f.write(json.dumps(res, indent=2))

if __name__ == '__main__':
    main()
