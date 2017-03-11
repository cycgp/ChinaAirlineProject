import jieba
import json
import logging
import sys

from gensim import corpora, models, similarities

ret = open("Aviation-1-2.json", "rb").read()
seglist = jieba.cut(ret, cut_all=False)

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
dictionary = corpora.Dictionary(ret)

hash = {}
for item in seglist: 
	if item in hash:
		hash[item] += 1
	else:
		hash[item] = 1
	fd = open("count.csv", "w", newline='', encoding='utf-8')
	fd.write("word,count\n")
	for k in hash:
		fd.write("%s,%d\n" % (k, hash[k]))
		print(k)