import json

with open('data.json') as data_file:
    datas = json.load(data_file)

outfile =  open('data.txt', 'w', encoding = 'utf-8')
for data in datas:
    outfile.write('乘坐'+data['class']+'，從'+data['origin']+'到'+data['destination']+'。'+data['title']+'。'+data['comment'])
