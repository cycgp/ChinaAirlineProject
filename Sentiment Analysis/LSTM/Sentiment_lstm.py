# -*- coding: utf-8 -*-
import yaml
import sys
from imp import reload
reload(sys)
from sklearn.model_selection import train_test_split
import multiprocessing
import numpy as np
from gensim.models.word2vec import Word2Vec
from gensim.corpora.dictionary import Dictionary
from keras.preprocessing import sequence
from keras.models import Sequential
from keras.layers.embeddings import Embedding
from keras.layers.recurrent import LSTM
from keras.layers.core import Dense, Dropout,Activation
from keras.models import model_from_yaml
np.random.seed(1337)  # For Reproducibility
import jieba
import pandas as pd
import sys
sys.setrecursionlimit(1000000)
# set parameters:
maxlen = 500
cpu_count = multiprocessing.cpu_count()

def create_dictionaries(model = None, combined = None):
	''' Function does are number of Jobs:
		1- Creates a word to index mapping
		2- Creates a word to vector mapping
		3- Transforms the Training and Testing Dictionaries
	'''
	if (combined is not None) and (model is not None):
		gensim_dict = Dictionary()
		gensim_dict.doc2bow(model.vocab.keys(),
							allow_update=True)
		w2indx = {v: k+1 for k, v in gensim_dict.items()}
		w2vec = {word: model[word] for word in w2indx.keys()}

		def parse_dataset(combined):
			''' Words become integers
			'''
			data=[]
			for sentence in combined:
				new_txt = []
				for word in sentence:
					try:
						new_txt.append(w2indx[word])
					except:
						new_txt.append(0)
				data.append(new_txt)
			return data
		combined = parse_dataset(combined)
		combined = sequence.pad_sequences(combined, maxlen=maxlen)
		return w2indx, w2vec,combined
	else:
		print('No data provided...')

def input_transform(inputList):
	transList = []
	model = Word2Vec.load('../docs/lstm_data/Word2vec_model.pkl')
	for string in inputList:
		words = jieba.lcut(string)
		words = np.array(words).reshape(1,-1)
		_,_,combined = create_dictionaries(model,words)
		transList.append(combined)
	return transList

def lstm_predict(inputList):
	print('loading model......')
	with open('../docs/lstm_data/lstm.yml', 'r') as f:
		yaml_string = yaml.load(f)
	model = model_from_yaml(yaml_string)

	print('loading weights......')
	model.load_weights('../docs/lstm_data/lstm.h5')
	model.compile(loss = 'binary_crossentropy',optimizer = 'adam',metrics = ['accuracy'])
	transList = input_transform(inputList)
	scoreList= []
	for data in transList:
		data.reshape(1,-1)
		result = model.predict_classes(data, verbose=0)
		prob = model.predict_proba(data, verbose=0)
		if result[0][0] == 1:
			score = prob[0][0]
		else:
			score = prob[0][0]*-1
		scoreList.append(score)
	return scoreList

if __name__=='__main__':
	input_data = ['航班準时,空服员亲切有礼,能给予我适合的服务,对於我的问题可以很清楚的答覆并解决,是我旅行传统航空得首选',
			'十分不好的飞行经验，飞机上居然没有乾净新的枕头和毛毯，所有东西都是之前旅客用过的，十分的糟糕，餐食普普通通',
			'普普通通，可能我抱的期待太大了，之前時常在報章雜誌上看到長榮獲獎的新聞，心裡想這間航空公司一定很棒!但真正飛行過後覺得與外界所說的稍微有點出入，我想可能我抱的期待太大了吧?但不得不說硬體設備真的很優!不過餐點部分就見仁見智了，從台灣飛往泰國所提供的餐點我覺得普普，但是從泰國飛往荷蘭這段所提供的餐點我真的覺得很棒(雞肉飯非常香辣又很下飯!)去程時(泰國飛往荷蘭)的空服員都很親切，而且非常親民很像鄰家姐姐般!但是回程時，不知道是因為有乘客在機上購買大量免稅品(?)使得事務長太開心並大聲直呼感謝，總而言之和朋友睡覺睡一半就被"謝謝"給喚醒來了...(我坐的位置是在左邊靠窗處，而當時那位事務長所站的地方是在另一邊的安全門位置)最後想繼續睡也睡不著，那就乾脆享受機上的硬體設備吧!',
			'沒有特別，整體而言服務還可以，沒有特別感覺。一開始很驚訝經濟艙有飲料單，但送餐時要求單上的品項又被空服員勸退，我跟她說我可以等沒關係，但後來送上的飲料很難喝。']
	print(lstm_predict(input_data))
