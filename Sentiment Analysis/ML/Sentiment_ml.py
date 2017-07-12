#coding:utf8
import jieba
#import nltk
import nltk
from nltk.collocations import  BigramCollocationFinder
from nltk.metrics import  BigramAssocMeasures
from nltk.probability import  FreqDist,ConditionalFreqDist
from nltk.metrics import  BigramAssocMeasures
#import sci-kit learn
import sklearn
from sklearn.externals import joblib

#get original text
def text():
	f1 = open('../docs/test.txt','r',encoding='utf8')
	line1 = f1.readline()
	str = ''

	while line1:
		str += line1
		line1 = f1.readline()
	f1.close()
	str = str.split('\n')
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

def jieba_best_words():
	posWords = []
	negWords = []

	for items in read_file('../docs/pos_tw.txt'):#把集合的集合變成集合
		for item in items:
			if item is not None:
				item = item.replace('\ufeff','').replace('\n','')
				posWords.append(item)

	for items in read_file('../docs/neg_tw.txt'):
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
	best_vals = sorted(word_scores.items(), key=lambda item:item[1],  reverse=True)[:1500] #把詞按資訊量倒序排序。number是特徵的維度
	best_words = set([w for w,s in best_vals])
	return dict([(word, True) for word in best_words])

def extract_features(datas):
	print('Extracting features...')
	feature = jieba_best_words()
	corpusFeatures = []
	for data in datas:
		a = {}
		for item in data:
			item = item.replace('\ufeff','')
			if item in feature.keys() and item is not '\n':
				a[item]='True'
		FeatureWords = a
		corpusFeatures.append(FeatureWords)
	return corpusFeatures

if __name__ == "__main__":

	jieba.set_dictionary('../docs/jieba_dict/dict.txt.big')

	#get corpus
	corpus = read_file('../docs/test.txt')
	corpusFeatures = extract_features(corpus)
	#classifier
	clf = joblib.load('../docs/ml_data/LogisticRegression_classifier.pkl')
	pred = clf.prob_classify_many(corpusFeatures)

	originalText = text()
	for i in pred:
		print('\n---\n' + str(pred.index(i)+1) + '\n---\nOriginal Text:\n')
		print(originalText[pred.index(i)].replace('\ufeff',''))
		print(corpusFeatures[pred.index(i)])
		print('Positive probability: %2.5f' %i.prob('pos'))
		print('Negative probability: %2.5f' %i.prob('neg'))
		score = i.prob('pos')-i.prob('neg')
		print('score: ' + str(score))
		print('Emotion: ' + i.max())
