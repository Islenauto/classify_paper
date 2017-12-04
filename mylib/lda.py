#-*- encoding: UTF-8 -*-
from gensim import corpora,models,similarities
import nltk
import treetaggerwrapper as ttw
import re,sys,os
import datacontroler as dtct

root_path = os.path.dirname(os.getcwd())

class Lda:
    def __init__(self,articles):

        texts = [article['sentence'] for article in articles]

                                                        
        # モデル作成用のdictionary,corpus作成
        dictionary = corpora.Dictionary(texts)
        dictionary.save(root_path+"/data/bbc.dict")
        
        corpus = [dictionary.doc2bow(text) for text in texts]
        tfidf = models.TfidfModel(corpus)
        corpus_tfidf = tfidf[corpus]
        
        # gensimのldaモデル作成
        self.lda = models.ldamodel.LdaModel(corpus=corpus_tfidf, num_topics=6,id2word=dictionary)
        self.hdp = models.hdpmodel.HdpModel(corpus=corpus_tfidf,id2word=dictionary,T=150)

        # 各doc内のトピック分布をリストに保存
        self.topics_indoc = [dict(self.hdp[c]) for c in corpus_tfidf]
