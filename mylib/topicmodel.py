#-*- encoding: UTF-8 -*-
from gensim import corpora,models,similarities
import nltk
import treetaggerwrapper as ttw
import re,sys,os

root_path = os.path.dirname(os.getcwd())

class TopicModel:
    def __init__(self,articles):

        self.data_original = [article['sentence_preprocessed'] for article in articles]
        self.data_parsed = [article['sentence'] for article in articles]

                                                        
        # モデル作成用のdictionary,corpus作成
        dictionary = corpora.Dictionary(self.data_parsed)
        #dictionary.save(root_path+"/data/bbc.dict")
        corpus = [dictionary.doc2bow(text) for text in self.data_parsed]
        #corpora.MmCorpus.serialize(root_path + "/data/corpus.mm",corpus)
        
        #dictionary = corpora.Dictionary.load(root_path+"/data/bbc.dict")
        #corpus = corpora.MmCorpus(root_path + "/data/corpus.mm")
        tfidf = models.TfidfModel(corpus)
        corpus_tfidf = tfidf[corpus]
        
        # gensimのldaモデル作成
        self.lda = models.ldamodel.LdaModel(corpus=corpus_tfidf, num_topics=6,id2word=dictionary)
        self.hdp = models.hdpmodel.HdpModel(corpus=corpus_tfidf,id2word=dictionary,T=150)

        # 各doc内のトピック分布リスト
        self.topics_indoc = [dict(self.hdp[c]) for c in corpus_tfidf]
        # トピック毎の各単語の生起確率リスト
        temp = [topic for topic in self.hdp.show_topics(num_topics=-1,num_words=len(dictionary),formatted=False)]
        self.W_Theta = [{w_theta[0]:w_theta[1] for w_theta in W_theta} for num,W_theta in temp]
