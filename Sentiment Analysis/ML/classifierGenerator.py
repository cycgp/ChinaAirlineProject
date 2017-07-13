#coding:utf-8
import jieba
#import nltk
import nltk
from nltk.collocations import  BigramCollocationFinder
from nltk.metrics import  BigramAssocMeasures
from nltk.probability import  FreqDist,ConditionalFreqDist
from nltk.metrics import  BigramAssocMeasures
#import sci-kit learn
import sklearn
from sklearn.naive_bayes import  MultinomialNB
from sklearn.linear_model import  LogisticRegression, SGDClassifier
from sklearn.externals import joblib
from nltk.classify.scikitlearn import  SklearnClassifier
#word list shuffle
from random import shuffle

#Generate corpus
def read_file(filename):
	jieba.load_userdict("../docs/jieba_dict/userdict.txt")
	stop = [line.strip() for line in  open('../docs/jieba_dict/stopwords.txt','r',encoding='utf-8').readlines()]#停用詞
	f = open(filename,'r',encoding='utf-8')
	line = f.readline()
	str = []

	while line:
		s = line.split('\t')
		fenci = jieba.cut(s[0], cut_all=False)#False預設值：精準模式
		str.append(list(set(fenci)-set(stop)))
		line = f.readline()
	return str

def jieba_feature(number):
	posWords = []
	negWords = []

	for items in read_file('./docs/tripadvisor_data/ignore_three_star/pos_tw.txt'):#把集合的集合變成集合
		for item in items:
			posWords.append(item)

	for items in read_file('./docs/tripadvisor_data/ignore_three_star/neg_tw.txt'):
		for item in items:
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

def build_features(topRank):
	feature = jieba_feature(topRank)
	posFeatures = []
	for items in read_file('./docs/tripadvisor_data/ignore_three_star/pos_tw.txt'):
		a = {}
		for item in items:
			if item in feature.keys():
				a[item]='True'
		posWords = [a,'pos'] #為積極文字賦予"pos"
		posFeatures.append(posWords)
	negFeatures = []

	for items in read_file('./docs/tripadvisor_data/ignore_three_star/neg_tw.txt'):
		a = {}
		for item in items:
			if item in feature.keys():
				a[item]='True'
		negWords = [a,'neg'] #為消極文字賦予"neg"
		negFeatures.append(negWords)
	return posFeatures,negFeatures

if __name__ == "__main__":
	jieba.set_dictionary('../docs/jieba_dict/dict.txt.big')

	posFeatures,negFeatures =  build_features(6000)#獲得訓練資料
	train =  posFeatures+negFeatures
	MultinomialNB_classifier = SklearnClassifier(MultinomialNB()) #在nltk中使用scikit-learn的介面
	MultinomialNB_classifier.train(train) #訓練分類器
	joblib.dump(MultinomialNB_classifier, '../docs/ml_data/MultinomialNB_classifier.pkl')

	posFeatures,negFeatures =  build_features(1000)#獲得訓練資料
	train =  posFeatures+negFeatures
	LogisticRegression_classifier = SklearnClassifier(LogisticRegression()) #在nltk中使用scikit-learn的介面
	LogisticRegression_classifier.train(train) #訓練分類器
	joblib.dump(LogisticRegression_classifier, '../docs/ml_data/LogisticRegression_classifier.pkl')

	print('Done!')
