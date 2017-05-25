#coding:utf-8
import json

with open('data_CI.json', encoding = 'utf-8') as data_file:
    datas = json.load(data_file)

outfile =  open('data_CI.txt', 'w', encoding = 'utf-8')
for data in datas:
    outfile.write('乘坐'+data['class']+'，從'+data['origin']+'到'+data['destination']+'。'+data['title']+'。'+data['comment'])

with open('data_CX.json', encoding = 'utf-8') as data_file:
    datas = json.load(data_file)

outfile =  open('data_CX.txt', 'w', encoding = 'utf-8')
for data in datas:
    outfile.write('乘坐'+data['class']+'，從'+data['origin']+'到'+data['destination']+'。'+data['title']+'。'+data['comment'])


with open('data_BR.json', encoding = 'utf-8') as data_file:
    datas = json.load(data_file)

outfile =  open('data_BR.txt', 'w', encoding = 'utf-8')
for data in datas:
    outfile.write('乘坐'+data['class']+'，從'+data['origin']+'到'+data['destination']+'。'+data['title']+'。'+data['comment'])


with open('data_SQ.json', encoding = 'utf-8') as data_file:
    datas = json.load(data_file)

outfile =  open('data_SQ.txt', 'w', encoding = 'utf-8')
for data in datas:
    outfile.write('乘坐'+data['class']+'，從'+data['origin']+'到'+data['destination']+'。'+data['title']+'。'+data['comment'])

