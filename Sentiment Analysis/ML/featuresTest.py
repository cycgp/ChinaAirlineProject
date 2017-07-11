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
from sklearn.svm import SVC, LinearSVC,  NuSVC
from sklearn.naive_bayes import  MultinomialNB, BernoulliNB
from sklearn.linear_model import  LogisticRegression
from sklearn.metrics import  accuracy_score
#word list shuffle
from random import shuffle

def text():
    f1 = open('../docs/pos_tw.txt','r',encoding='utf-8')
    f2 = open('../docs/neg_tw.txt','r',encoding='utf-8')
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

def bag_of_words(words):
    return dict([(word,True) for word in words])

def bigram(words,score_fn=BigramAssocMeasures.chi_sq,n=1000):
    bigram_finder=BigramCollocationFinder.from_words(words)#把文字變成雙詞搭配的形式
    bigrams = bigram_finder.nbest(score_fn,n)#使用卡方統計的方法，選擇排名前1000的雙詞
    newBigrams = [u+v for (u,v) in bigrams]
    return bag_of_words(newBigrams)
#print(bigram(text(),score_fn=BigramAssocMeasures.chi_sq,n=1000))

def bigram_words(words,score_fn=BigramAssocMeasures.chi_sq,n=1000):
    bigram_finder=BigramCollocationFinder.from_words(words)
    bigrams = bigram_finder.nbest(score_fn,n)
    newBigrams = [u+v for (u,v) in bigrams]
    a = bag_of_words(words)
    b = bag_of_words(newBigrams)
    a.update(b)#把字典b合併到字典a中
    return a#所有單個詞和雙個詞一起作為特徵
#print(bigram_words(text(),score_fn=BigramAssocMeasures.chi_sq,n=1000))

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

    for items in read_file('../docs/pos_tw.txt'):#把集合的集合變成集合
        for item in items:
            posWords.append(item)

    for items in read_file('../docs/neg_tw.txt'):
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
    best_vals = sorted(word_scores.items(), key=lambda item:item[1],  reverse=True)[:number] #把詞按資訊量倒序排序。number是特徵的維度，是可以不斷調整直至最優的
    best_words = set([w for w,s in best_vals])
    return dict([(word, True) for word in best_words])

def build_features(feature_info, topRank):
    if feature_info == 0:
        feature = bag_of_words(text())#单个词
    elif feature_info == 1:
        feature = bigram(text(),score_fn=BigramAssocMeasures.chi_sq,n=topRank)#双个词
    elif feature_info == 2:
        feature =  bigram_words(text(),score_fn=BigramAssocMeasures.chi_sq,n=topRank)#单个词和双个词
    else:
        feature = jieba_feature(topRank)

    posFeatures = []
    for items in read_file('../docs/pos_tw.txt'):
        a = {}
        for item in items:
            if item in feature.keys():
                a[item]='True'
        posWords = [a,'pos'] #為積極文字賦予"pos"
        posFeatures.append(posWords)
    negFeatures = []

    for items in read_file('../docs/neg_tw.txt'):
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

    jieba.set_dictionary('../docs/jieba_dict/dict.txt.big')
    TOPRANK = [500, 1000, 1500, 2000]
    FEATURES_INFO = ['Bag Of Words', 'Bigram', 'Bigram Words', 'Jieba Feature']
    features = [0, 1, 2, 3]

    #test
    posFeatures,negFeatures =  build_features(jieba_feature, 100)

    for feature in features:
        j = 1
        feature_info = FEATURES_INFO[feature]
        print('\n------ '+feature_info+' -------')
        for n in TOPRANK:
            posFeatures,negFeatures =  build_features(feature, n)#獲得訓練資料
            posLength = int(len(posFeatures)*0.8)
            negLength = int(len(negFeatures)*0.8)

            shuffle(posFeatures) #把文本的排列随机化
            shuffle(negFeatures) #把文本的排列随机化

            train =  posFeatures[:posLength]+negFeatures[:negLength]#訓練集(80%)
            test = posFeatures[posLength:]+negFeatures[negLength:]#預測集(驗證集)(20%)

            data,tag = zip(*test)#分離測試集合的資料和標籤，便於驗證和測試
            if j == 1:
                print('\nn\tBernoulliNB\tMultinomiaNB\tSVC\t\tLinearSVC\tLogisticRegression')
            j = 2
            print('%4.0f\t%6.6f\t%6.6f\t%6.6f\t%6.6f\t%6.6f' %(n, score(BernoulliNB()), score(MultinomialNB()), score(SVC()), score(LinearSVC()), score(LogisticRegression())))
