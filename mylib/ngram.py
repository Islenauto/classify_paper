# -*- encoding: UTF-8 -*-
import re,nltk,sys
from tqdm import tqdm
import numpy as np
import pandas as pd
from gensim import corpora,models,similarities
from itertools import chain

class Ngram:
    def __init__(self,texts,n=2):
        
        self.n = n # n-gram
        self.texts_orig = texts # 処理前の文書
        self.texts_ngram = [list(nltk.ngrams(text,self.n)) for text in texts] #各文書のngramリスト(ex.('apple','tree'))
        self.texts_sub1gram = [list(nltk.ngrams(text,self.n-1)) for text in texts] #各文書のn-1gramリスト
        self.dic_tf_ngram = self.create_tfdic(self.texts_ngram) # 各ngramのtf辞書
        self.dic_tf_sub1gram = self.create_tfdic(self.texts_sub1gram) # n-1gramのtf辞書
        

    # 最尤推定
    def mle(self):
        
        dic_mle = {}
        for ngram,tf in self.dic_tf_ngram.items():
            if self.n>1: sub1gram = '-'.join(ngram.split('-')[:-1])
            c_ngram = tf # ngramの頻度
            c_sub1gram = self.dic_tf_sub1gram[sub1gram] if self.n>1 else len(self.dic_tf_sub1gram) # n-1gramの頻度
            dic_mle[ngram] = c_ngram / c_sub1gram
        return dic_mle

    
    # 共起回数をカウント
    def count_cooccur(self,w1,w2):
        
        count = 0
        for ngram in self.target:
            if w1 in ngram and w2 in "-".join(ngram):
                count += 1
        return count   


    # 共起回数の辞書を作成(search_window:探索幅，complex_term:共起対象に複合語が含まれるか)
    def make_dic_cooccur(self,words_1,words_2,targets,search_window=2,complex_term=False):

        search_window = self.n + 1 if complex_term else 2
        self.target = list(chain.from_iterable([list(nltk.ngrams(target,search_window)) for target in targets]))

        dic_cooccur = {}
        for w1 in tqdm(words_1):
            dic_cooccur[w1] = {w2: self.count_cooccur(w1,w2) for w2 in words_2}
        return dic_cooccur
    

    # t値の算出
    def t_score(self,w_target,w_cooccur,dic_cooccur):
        
        frq_cooccur = dic_cooccur[w_target][w_cooccur]  # 共起頻度
        frq_w_tag = self.dic_tf_sub1gram[w_target] # 中心語頻度
        frq_w_cooccur = self.dic_tf_sub1gram[w_cooccur] # 共起語頻度
        sum_tf = sum(self.dic_tf_sub1gram.values()) # 総語数
        ave_frq_cooccur = (frq_w_tag * frq_w_cooccur) / sum_tf # 共起頻度期待値

        t = (frq_cooccur - ave_frq_cooccur) / np.sqrt(frq_cooccur) # t値
        return t
    

    # tf辞書作成
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


    # tfリスト,id-単語を紐付けた辞書の作成(create_tfの補助メソッド)
    def create_tflis(self,texts4dic,texts4corpus):
        
        if isinstance(texts4corpus[0],str): texts4corpus = [texts4corpus]
        dic_word2id = corpora.Dictionary(texts4dic)
        corpus_tf = [dic_word2id.doc2bow(text) for text in texts4corpus]
        return dic_word2id,corpus_tf
