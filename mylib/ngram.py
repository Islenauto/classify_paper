# -*- encoding: UTF-8 -*-
import nltk
from gensim import corpora,models,similarities
from mylib.datacontroler import DataControler
from mylib.topicmodel import TopicModel

class Ngram:
    def __init__(self,texts,n=2):
        
        self.n = n # n-gram
        self.texts_ngram = [list(nltk.ngrams(text,self.n)) for text in texts] #各文書のngramリスト(ex.('apple','tree'))
        self.texts_sub1gram = [list(nltk.ngrams(text,self.n-1)) for text in texts] #各文書のn-1gramリスト
        self.dic_tf_ngram = self.create_tfdic(self.texts_ngram)
        self.dic_tf_sub1gram = self.create_tfdic(self.texts_sub1gram)
        

    # 最尤推定(dist = binominal)
    def mle(self):
        
        dic_mle = {}
        for ngram,tf in self.dic_tf_ngram.items():
            sub1gram = '-'.join(ngram.split('-')[:-1]) if self.n>1 else ngram #1gramの場合はngram自身
            c_ngram = tf # ngramの頻度
            c_sub1gram = self.dic_tf_sub1gram[sub1gram] # n-1gramの頻度
            dic_mle[ngram] = c_ngram / c_sub1gram
        return dic_mle

    def create_tfdic(self,texts4dic):
        
        texts_ngram_joined = []  #各ngramを単一の文字列としたリスト(ex.['apple-tree','tree-under'],...)
        for ngrams in texts4dic:
            temp_ngram = ['-'.join(ngram) for ngram in ngrams]
            texts_ngram_joined.append(temp_ngram)
        texts4dic = texts_ngram_joined
        texts4corpus = DataControler().flatten_list(texts4dic)
        dic_word2id,lis_tf = self.create_tflis(texts4dic,texts4corpus)
        
        dic_tf = {dic_word2id[word_id]:tf for word_id,tf in lis_tf[0]}
        return dic_tf

    def create_tflis(self,texts4dic,texts4corpus):
        
        if isinstance(texts4corpus[0],str): texts4corpus = [texts4corpus]
        dic_word2id = corpora.Dictionary(texts4dic)
        corpus_tf = [dic_word2id.doc2bow(text) for text in texts4corpus]
        return dic_word2id,corpus_tf
