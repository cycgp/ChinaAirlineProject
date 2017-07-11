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
from nltk.classify.scikitlearn import  SklearnClassifier
from sklearn.svm import SVC, LinearSVC
from sklearn.naive_bayes import  MultinomialNB, BernoulliNB
from sklearn.linear_model import  LogisticRegression, SGDClassifier
from sklearn.metrics import  accuracy_score
#word list shuffle
from random import shuffle
#pandas
from pandas import Series, DataFrame
import pandas as pd
from tabulate import tabulate

def text():
    f1 = open('../docs/test/pos_tw.txt','r',encoding='utf-8')
    f2 = open('../docs/test/neg_tw.txt','r',encoding='utf-8')
    line1 = f1.readline()
    line2 = f2.readline()
    str = ''

    while line1:
        str += line1
        line1 = f1.readline()
    while line2:
        str += line2
        line2 = f2.readline()
    f1.close()
    f2.close()
    return str

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

    for items in read_file('../docs/test/pos_tw.txt'):#把集合的集合變成集合
        for item in items:
            posWords.append(item)

    for items in read_file('../docs/test/neg_tw.txt'):
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
    for items in read_file('../docs/test/pos_tw.txt'):
        a = {}
        for item in items:
            if item in feature.keys():
                a[item]='True'
        posWords = [a,'pos'] #為積極文字賦予"pos"
        posFeatures.append(posWords)
    negFeatures = []

    for items in read_file('../docs/test/neg_tw.txt'):
        a = {}
        for item in items:
            if item in feature.keys():
                a[item]='True'
        negWords = [a,'neg'] #為消極文字賦予"neg"
        negFeatures.append(negWords)
    return posFeatures,negFeatures

def score(classifier):
    classifier = SklearnClassifier(classifier) #在nltk中使用scikit-learn的介面
    classifier.train(train) #訓練分類器
    pred = classifier.classify_many(data) #對測試集的資料進行分類，給出預測的標籤
    accuracy = nltk.classify.accuracy(classifier,test)
    return accuracy #對比分類預測結果和人工標註的正確結果，給出分類器準確度

if __name__ == "__main__":

    TOPRANK = [1000, 2000, 3000, 4000, 5000, 6000, 7000]

    accuracyScores = []
    for i in range(0,6):
        accuracyScore = []
        for j in range(0,7):
            accuracyScore.append(0)
        accuracyScores.append(accuracyScore)

    jieba.set_dictionary('../docs/jieba_dict/dict.txt.big')

    #執行100次
    for i in range(0,10):
        for n in range(0,len(TOPRANK)):
            posFeatures,negFeatures =  build_features(TOPRANK[n])#獲得訓練資料
            posLength = int(len(posFeatures)*0.8)
            negLength = int(len(negFeatures)*0.8)

            shuffle(posFeatures) #把文本的排列随机化
            shuffle(negFeatures) #把文本的排列随机化

            train =  posFeatures[:posLength]+negFeatures[:negLength]#訓練集(80%)
            test = posFeatures[posLength:]+negFeatures[negLength:]#預測集(驗證集)(20%)

            data,tag = zip(*test)#分離測試集合的資料和標籤，便於驗證和測試

            accuracyScores[0][n] += score(BernoulliNB())
            accuracyScores[1][n] += score(MultinomialNB())
            accuracyScores[2][n] += score(SVC())
            accuracyScores[3][n] += score(LinearSVC())
            accuracyScores[4][n] += score(LogisticRegression())
            accuracyScores[5][n] += score(SGDClassifier())
        print(i)

    print('\nAccuracyScores...\n')
    datas = {'BernoulliNB': accuracyScores[0],
        'MultinomialNB': accuracyScores[1],
        'SVC': accuracyScores[2],
        'LinearSVC': accuracyScores[3],
        'LogisticRegression': accuracyScores[4],
        'SGDClassifier': accuracyScore[5]
        }

    df = pd.DataFrame(datas, index=['1000', '2000', '3000', '4000', '5000', '6000', '7000'])
    print(tabulate(df, headers='keys', tablefmt='psql'))



    # print('\nn\tBernoulliNB\tMultinomiaNB\tSVC\t\tLinearSVC\tLogisticRegression')
    # print('%4.0f\t%6.6f\t%6.6f\t%6.6f\t%6.6f\t%6.6f' %(n, score(BernoulliNB()), score(MultinomialNB()), score(SVC()), score(LinearSVC()), score(LogisticRegression())))
