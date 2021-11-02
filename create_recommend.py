import json

data = None

with open('qiita_nimi_data.json', encoding='utf-8') as f:
    data = json.load(f)

top = ['Python', 'JavaScript', 'Ruby', 'Rails', 'AWS', 'PHP', 'Docker', 'iOS', 'Java', 'Swift', '初心者', 'Android', 'Linux', 'Node.js', 'Python3', 'Git', 'C#', 'Unity', 'Mac', 'CSS', 'Vue.js', 'Go', 'MySQL', 'Laravel', 'HTML', 'React', '機械学習', 'C++', 'Windows', 'GitHub', 'Xcode', 'TypeScript', 'RaspberryPi', 'Ubuntu', 'CentOS', 'DeepLearning', 'jQuery', 'Bash', 'VSCode', 'Kotlin', 'Azure', 'kubernetes', 
'MacOSX', 'Firebase', 'Vim', 'Vagrant', 'WordPress', 'SQL', 'Django', 'Heroku', 'Objective-C', 'R', 'PostgreSQL', 'lambda', 'Windows10', '#migrated', 'Slack', 'nginx', 'TensorFlow', 'HTML5', 'C', 'EC2', 'docker-compose', 'Excel', 'IoT', 'gcp', 'Angular', 'ShellScript', 'Scala', 'GoogleAppsScript', 'AtCoder', 'centos7', 'Flutter', 'Arduino', 'nuxt.js', 'api', 'SSH', 'OpenCV', 'ポエム', 'PowerShell', 'MachineLearning', 'Ansible', 'Apache', 'AndroidStudio', 
'競技プログラミング', '新人プログラマ応援', 'Rust', 'Chrome', 'VirtualBox', 'JSON', 'oracle', 'pandas', '初心者向け', 'S3', 'VBA', 'Qiita', 'Elixir', 'npm', 'spring-boot', '数学'
]

output_data = []

for tag in top:
    tag_cnt = []
    for obj in data:
        flag = False
        for tg in obj['tags']:
            if(tg['name'] == tag):
                flag = True
        if(flag == True):
            object = {}
            object['title'] = obj['title']
            object['url'] = obj['url']
            object['likes_count'] = obj['likes_count']
            tag_cnt.append(object)
    tag_cnt = sorted(tag_cnt, key=lambda x:x['likes_count'], reverse=True)

    output_obj = {}
    output_obj['type'] = tag
    output_obj['title'] = []
    output_obj['url'] = []
    for i in range(10):
        output_obj['title'].append(tag_cnt[i]['title'])
        output_obj['url'].append(tag_cnt[i]['url'])
    output_data.append(output_obj)
print(output_data)

with open('output.json', 'w', encoding='utf-8') as f:
    json.dump(output_data, f, ensure_ascii=False, indent=2)
