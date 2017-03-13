from gensim.models import word2vec
import logging

def main():

    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    sentences = word2vec.Text8Corpus("data_seg.txt")
    model = word2vec.Word2Vec(sentences, size=2)

    #保存模型，供日後使用
    model.wv.save_word2vec_format(u"med250.model.bin", binary=True)

    #模型讀取方式
    # model = word2vec.Word2Vec.load_word2vec_format("your_model.bin", binary=True)

if __name__ == "__main__":
    main()
