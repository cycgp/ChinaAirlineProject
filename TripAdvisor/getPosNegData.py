#conding:utf-8
import json

datas = []

with open('data.json') as json_data:
    datas = json.load(json_data)

pos = open("pos.txt","w")
neg = open("neg.txt","w")

for data in datas:
    if int(data['rating']) >= 4:
        pos.write(data['title']+'，'+data['comment']+'\n')
    else:
        neg.write(data['title']+'，'+data['comment']+'\n')

pos.close()
neg.close()
