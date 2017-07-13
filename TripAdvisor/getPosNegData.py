#conding:utf-8
import json

datas = []

with open('./data_json/data.json', encoding='utf-8') as json_data:
    datas = json.load(json_data)

pos = open("data_txt/pos.txt","w", encoding='utf-8')
neg = open("data_txt/neg.txt","w", encoding='utf-8')

for data in datas:
    if int(data['rating']) > 3:
        pos.write(data['title']+'，'+data['comment']+'\n')
    elif int(data['rating']) < 3:
        neg.write(data['title']+'，'+data['comment']+'\n')

pos.close()
neg.close()
