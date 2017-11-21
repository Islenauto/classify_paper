#-*- encoding: UTF-8 -*-
from gensim import corpora,models,similarities
import nltk
import treetaggerwrapper as ttw
import re,sys,os
import datacontroler as dtct

root_path = os.path.dirname(os.getcwd())

class Lda:
    def __init__(self,num_topics,name_news,category):
        self.name_news = name_news
        self.category = category

        content_dic = dtct.DataControler().import_data(self.name_news,self.category)
        texts = [dic['sentence'] for dic in content_dic]

                                                        
        # モデル作成用のdictionary,corpus作成
        dictionary = corpora.Dictionary(texts)
        dictionary.save(root_path+"/data/bbc.dict")
        
        corpus = [dictionary.doc2bow(text) for text in texts]
        tfidf = models.TfidfModel(corpus)
        corpus_tfidf = tfidf[corpus]
        
        # gensimのldaモデル作成
        self.lda = models.ldamodel.LdaModel(corpus=corpus_tfidf, num_topics=num_topics,id2word=dictionary)
        self.hdp = models.hdpmodel.HdpModel(corpus=corpus_tfidf,id2word=dictionary)
