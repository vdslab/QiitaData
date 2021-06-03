import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

data = pd.read_csv("simpson_data_100.csv")
data = np.array(np.mat(data))
for i in range(100):
    for j in range(100):
        data[i][j] = 1 - data[i][j]

#全体のラベル
dumy_labels = ["Python","JavaScript","Ruby","Rails","AWS","PHP","Docker","iOS","Java","Swift","shosinnsha","Android","Linux","Node.js","Python3","Git","C#","Unity","Mac","CSS","Vue.js","Go","MySQL","Laravel","HTML","React","kikaigakushu","C++","Windows","GitHub","TypeScript","Xcode","RaspberryPi","Ubuntu","CentOS","DeepLearning","jQuery","Bash","VSCode","Kotlin","Azure","kubernetes","MacOSX","Firebase","Vim","Vagrant","SQL","WordPress","Django","Heroku","Objective-C","R","PostgreSQL","lambda","Windows10","#migrated","Slack","nginx","TensorFlow","HTML5","C","EC2","docker-compose","Excel","IoT","gcp","Angular","ShellScript","Scala","AtCoder","GoogleAppsScript","centos7","Flutter","Arduino","nuxt.js","api","SSH","OpenCV","poem","PowerShell","MachineLearning","Ansible","Apache","AndroidStudio","kyougi","ouen","Rust","Chrome","VirtualBox","JSON","oracle","pandas","shosinnmuke","S3","VBA","Qiita","Elixir","npm","spring-boot","math"]
#とりあえず表示したいラベル
labels = ["Python","JavaScript","Node.js","Python3","Vue.js", "HTML","React","TypeScript","DeepLearning","jQuery","Firebase","HTML5","Angular","JSON","pandas","npm"]

n = len(data)
s = data * data
one = np.eye(n) - np.ones((n, n)) / n
p = -1.0 / 2 * one * s * one

w, v = np.linalg.eig(p)
ind = np.argsort(w)
x1 = ind[-1] # 1番
x2 = ind[-2] # 2番

# 標準されたデータの固有値が求められているので標準偏差を掛けて可視化
s = p.std(axis=0)
w1 = s[x1]
w2 = s[x2]
for i in range(n):
    if dumy_labels[i] in labels:
        plt.text(w1 * v[i, x1], w2 * v[i, x2], dumy_labels[i])
    plt.plot(w1 * v[i, x1], w2 * v[i, x2], 'b.')
plt.draw()
plt.show()