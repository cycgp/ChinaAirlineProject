#coding:utf8
from sklearn.externals import joblib
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
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import time
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
	print('    Loading model -> DeepLearning_LSTM')
	with open('../docs/lstm_data/lstm.yml', 'r') as f:
		yaml_string = yaml.load(f)
	model = model_from_yaml(yaml_string)

	print('    Loading weights -> DeepLearning_LSTM')
	model.load_weights('../docs/lstm_data/lstm.h5')
	model.compile(loss = 'binary_crossentropy',optimizer = 'adam',metrics = ['accuracy'])
	print('    Transforming input data ...')
	transList = input_transform(inputList)
	print('    Classifying ( DeepLearning_LSTM) ...')
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

import jieba
import nltk
from nltk.collocations import  BigramCollocationFinder
from nltk.metrics import  BigramAssocMeasures
from nltk.probability import  FreqDist,ConditionalFreqDist
from nltk.metrics import  BigramAssocMeasures
import sklearn
from sklearn.externals import joblib
import pandas as pd

def read_csv_file():
	#fileName = '../docs/csv_data/NewsList_' + time.strftime('%Y%m%d', time.localtime()) + '.csv'
	fileName = '../docs/facebook_comments/FB_Data_comments_0301_final.csv'
	df = pd.read_csv(fileName)
	record = df['comment'].values.tolist()
	return record

#get original text
def read_csv_file_jieba():
	jieba.load_userdict("../docs/jieba_dict/userdict.txt")
	stop = [line.strip() for line in  open('../docs/jieba_dict/stopwords.txt','r',encoding='utf8').readlines()]#停用詞

	#fileName = '../docs/csv_data/NewsList_' + time.strftime('%Y%m%d', time.localtime()) + '.csv'
	fileName = '../docs/facebook_comments/FB_Data_comments_0301_final.csv'
	df = pd.read_csv(fileName)
	record = df['comment'].values.tolist()

	str = []
	for line in record:
		fenci = jieba.cut(line, cut_all=False)#False預設值：精準模式
		str.append(list(set(fenci)-set(stop)))
	return str

#Generate corpus
def read_file(filename):
	jieba.load_userdict("../docs/jieba_dict/userdict.txt")
	stop = [line.strip() for line in  open('../docs/jieba_dict/stopwords.txt','r',encoding='utf8').readlines()]#停用詞
	f = open(filename,'r',encoding='utf8')
	line = f.readline()
	str = []

	while line:
		s = line.split('\t')
		fenci = jieba.cut(s[0], cut_all=False)#False預設值：精準模式
		str.append(list(set(fenci)-set(stop)))
		line = f.readline()
	return str

def jieba_best_words(number):
	posWords = []
	negWords = []

	for items in read_file('../docs/tripadvisor_data/ignore_three_star/pos_tw.txt'):#把集合的集合變成集合
		for item in items:
			if item is not None:
				item = item.replace('\ufeff','').replace('\n','')
				posWords.append(item)

	for items in read_file('../docs/tripadvisor_data/ignore_three_star/neg_tw.txt'):
		for item in items:
			if item is not None:
				item = item.replace('\ufeff','').replace('\n','')
				negWords.append(item)

	word_fd = FreqDist() #可統計所有詞的詞頻
	cond_word_fd = ConditionalFreqDist() #可統計積極文字中的詞頻和消極文字中的詞頻

	for word in posWords:
		word_fd[word] += 1
		cond_word_fd['pos'][word] += 1

	for word in negWords:
		word_fd[word] += 1
		cond_word_fd['neg'][word] += 1

	pos_word_count = cond_word_fd['pos'].N() #積極詞的數量
	neg_word_count = cond_word_fd['neg'].N() #消極詞的數量
	total_word_count = pos_word_count + neg_word_count
	word_scores = {}#包括了每個詞和這個詞的資訊量

	for word, freq in word_fd.items():
		pos_score = BigramAssocMeasures.chi_sq(cond_word_fd['pos'][word],  (freq, pos_word_count), total_word_count) #計算積極詞的卡方統計量，這裡也可以計算互資訊等其它統計量
		neg_score = BigramAssocMeasures.chi_sq(cond_word_fd['neg'][word],  (freq, neg_word_count), total_word_count) #同理
		word_scores[word] = pos_score + neg_score #一個詞的資訊量等於積極卡方統計量加上消極卡方統計量
	best_vals = sorted(word_scores.items(), key=lambda item:item[1],  reverse=True)[:number] #把詞按資訊量倒序排序。number是特徵的維度
	best_words = set([w for w,s in best_vals])
	return dict([(word, True) for word in best_words])

def extract_features(datas, number):
	feature = jieba_best_words(number)
	corpusFeatures = []
	for data in datas:
		a = {}
		for item in data:
			item = item.replace('\ufeff','')
			if item in feature.keys() and item is not '\n':
				a[item]='True'
		posWords = a #為積極文字賦予"pos"
		corpusFeatures.append(posWords)
	return corpusFeatures

if __name__ == "__main__":
	jieba.set_dictionary('../docs/jieba_dict/dict.txt.big')

	#get corpus
	print('Reading CSV file......')
	corpus = read_csv_file()
	corpus_jieba = read_csv_file_jieba()
	corpusFeatures_LogisticRegression = extract_features(corpus_jieba, 1000)
	corpusFeatures_MultinomialNB = extract_features(corpus_jieba, 5000)
	#LogisticRegression_classifier
	print('\nLogisticRegression:')
	print('    Loading model -> LogisticRegression_classifier')
	LogisticRegression_classifier = joblib.load('../docs/ml_data/LogisticRegression_classifier.pkl')
	print('    Classifying ( LogisticRegression_classifier) ...')
	LogisticRegression_pred = LogisticRegression_classifier.prob_classify_many(corpusFeatures_LogisticRegression)
	#MultinomialNB_classifier
	print('\nMultinomialNB:')
	print('    Loading model -> MultinomialNB_classifier')
	MultinomialNB_classifier = joblib.load('../docs/ml_data/MultinomialNB_classifier.pkl')
	print('    Classifying ( MultinomialNB_classifier) ...')
	MultinomialNB_pred = MultinomialNB_classifier.prob_classify_many(corpusFeatures_MultinomialNB)
	print('\nLSTM:')
	DeepLearning_LSTM_score = lstm_predict(corpus)
	LogisticRegression_score = []
	MultinomialNB_score = []
	Sum = []
	emotion_sum = []
	emotion = []
	DeepLearning_emotion = []

	for i in LogisticRegression_pred:
		score = i.prob('pos')-i.prob('neg')
		LogisticRegression_score.append(score)

	for i in MultinomialNB_pred:
		score = i.prob('pos')-i.prob('neg')
		MultinomialNB_score.append(score)

	for i in range(0,len(MultinomialNB_score)):
		Sum.append(LogisticRegression_score[i] + MultinomialNB_score[i] + DeepLearning_LSTM_score[i])

	for data in Sum:
		if data > 0:
			emotion_sum.append('Positive')
		else:
			emotion_sum.append('Negative')

	for i in range(0,len(MultinomialNB_score)):
		L_score = LogisticRegression_score[i] > 0
		M_score = MultinomialNB_score[i] > 0
		D_score = DeepLearning_LSTM_score[i] > 0
		if sum([L_score, M_score, D_score]) > 1 :
			emotion.append('Positive')
		else:
			emotion.append('Negative')

	for data in LogisticRegression_score:
		if data > 0:
			DeepLearning_emotion.append(1)
		else:
			DeepLearning_emotion.append(-1)

	print('\nSaving Scores...')
	score = np.array([LogisticRegression_score, MultinomialNB_score, DeepLearning_LSTM_score, Sum, emotion_sum, emotion, DeepLearning_emotion]).transpose()
	print('Merging CSV file...')
	df1 = pd.DataFrame(data=score, columns=['LogisticRegression_score', 'MultinomialNB_score', 'DeepLearning_LSTM_score' , 'Sum', 'emotion_sum', 'emotion', 'DeepLearning_emotion'])
	#fileName = 'NewsList_20170713'
	fileName = 'FB_Data_comments_0301_final.csv'
	# df2 = pd.read_csv('../docs/csv_data/' + fileName + '.csv').join(df1, how='outer')
	df2 = pd.read_csv('../docs/facebook_comments/FB_Data_comments_0301_final.csv').join(df1, how='outer')

	df2.to_csv('../docs/csv_data_SA/'+fileName+'_SA.csv', sep=',', encoding='utf-8', index=False)
	print('\nDone!')
