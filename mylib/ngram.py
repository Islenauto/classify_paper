# -*- encoding: UTF-8 -*-
import re,nltk
from gensim import corpora,models,similarities
from itertools import chain

class Ngram:
    def __init__(self,texts,n=2):
        
        self.n = n # n-gram
        self.texts_orig = texts
        self.texts_ngram = [list(nltk.ngrams(text,self.n)) for text in texts] #各文書のngramリスト(ex.('apple','tree'))
        self.texts_sub1gram = [list(nltk.ngrams(text,self.n-1)) for text in texts] #各文書のn-1gramリスト
        self.dic_tf_ngram = self.create_tfdic(self.texts_ngram)
        self.dic_tf_sub1gram = self.create_tfdic(self.texts_sub1gram)
        

    # 最尤推定(dist = binominal)
    def mle(self):
        
        dic_mle = {}
        for ngram,tf in self.dic_tf_ngram.items():
            if self.n>1: sub1gram = '-'.join(ngram.split('-')[:-1])
            c_ngram = tf # ngramの頻度
            c_sub1gram = self.dic_tf_sub1gram[sub1gram] if self.n>1 else len(self.dic_tf_sub1gram) # n-1gramの頻度
            dic_mle[ngram] = c_ngram / c_sub1gram
        return dic_mle
    

    # 共起回数をカウント(探索幅=search_window,引数w1,w2が複合語であるか=complex_term)
    def count_cooccur(self,w1,w2,search_window=2,complex_term=False):
        
        count = 0
        if complex_term: search_window= search_window + 1
        target = list(chain.from_iterable([list(nltk.ngrams(text,search_window)) for text in self.texts_orig]))
        for ngram in target:
            ngram = '-'.join(ngram) # w1かw2が複合語の場合
            if w2 in ngram and w1 in ngram.replace('w2',''):
                count += 1
        return count   

    def create_tfdic(self,texts4dic):
        
        texts_ngram_joined = []  #各ngramを単一の文字列としたリスト(ex.['apple-tree','tree-under'],...)
        for ngrams in texts4dic:
            temp_ngram = ['-'.join(ngram) for ngram in ngrams]
            texts_ngram_joined.append(temp_ngram)
        texts4dic = texts_ngram_joined
        texts4corpus = list(chain.from_iterable(texts4dic))
        dic_word2id,lis_tf = self.create_tflis(texts4dic,texts4corpus)
        
        dic_tf = {dic_word2id[word_id]:tf for word_id,tf in lis_tf[0]}
        return dic_tf

    def create_tflis(self,texts4dic,texts4corpus):
        
        if isinstance(texts4corpus[0],str): texts4corpus = [texts4corpus]
        dic_word2id = corpora.Dictionary(texts4dic)
        corpus_tf = [dic_word2id.doc2bow(text) for text in texts4corpus]
        return dic_word2id,corpus_tf
