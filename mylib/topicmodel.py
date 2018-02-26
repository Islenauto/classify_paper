#-*- encoding: UTF-8 -*-
from gensim import corpora,models,similarities
import nltk
import pandas as pd
import treetaggerwrapper as ttw
import re,sys,os

root_path = os.path.dirname(os.getcwd())

class TopicModel:
    def __init__(self,tb_articles=None,update=False):
        # 既存のdictionary,corpus,modelが無い場合は新規作成
        if update == True:
            self.update_model(tb_articles)
        
        # dictionary,corpus,model読み込み 
        tb_articles = pd.read_excel(root_path+'/data/articles.xlsx')
        self.sentences_parsed = [row['sentence_parsed'].split("\t") for index,row in tb_articles.iterrows()]
        self.sentences_parsed_with_pos = [row['sentence_parsed_with_pos'].split("\t") for index,row in tb_articles.iterrows()]
        
        dictionary = corpora.Dictionary.load(root_path+'/data/articles.dict')
        corpus_tfidf = corpora.MmCorpus(root_path+'/data/articles.mm')
        self.hdp = models.hdpmodel.HdpModel.load(root_path+'/data/hdp.model')
        
        self.W = [word for word in dictionary.values()]
        self.topics_indoc = [dict(self.hdp[c]) for c in corpus_tfidf] # 各doc内のトピック分布リスト
        self.num_topics_indoc = pd.DataFrame(self.topics_indoc).shape[1] # トピック数 
        self.id_topics_indoc = list(pd.DataFrame(self.topics_indoc).columns) # 文書に割り当てがあるトピックのidリスト
        self.K = len(self.id_topics_indoc) # トピック数
        temp = [topic for topic in self.hdp.show_topics(num_topics=-1,num_words=len(dictionary),formatted=False)]
        self.W_Theta = {num:{w_theta[0]:w_theta[1] for w_theta in W_theta} for num,W_theta in temp} # トピック毎の各単語の生起確率辞書
        self.W_Theta_indoc = {num:{w_theta[0]:w_theta[1] for w_theta in W_theta} for num,W_theta in temp if num in self.id_topics_indoc} # トピック毎の各単語の生起確率辞書(文書に割り当てがあるもの)


    def create_tfcorpus(self,texts4dic,texts4corpus):
        # 単一文書の場合は多重リスト化(gensimのDictionaryの仕様上単一リストは受け付けない)
        if isinstance(texts4corpus[0],str): texts4corpus = [texts4corpus]
        dic_word2id = corpora.Dictionary(texts4dic)
        corpus_tf = [dic_word2id.doc2bow(text) for text in texts4corpus]
        return (dic_word2id,corpus_tf)


    def update_model(self,tb_articles):
        sentences_parsed = [row['sentence_parsed'].split("\t") for index,row in tb_articles.iterrows()]

        dictionary,corpus = self.create_tfcorpus(sentences_parsed,sentences_parsed)
        tfidf = models.TfidfModel(corpus)
        corpus_tfidf = tfidf[corpus]
        hdp = models.hdpmodel.HdpModel(corpus=corpus_tfidf,id2word=dictionary,T=30)

        tb_articles.to_csv(root_path+"/data/articles.csv")
        dictionary.save(root_path+'/data/articles.dict')
        corpora.MmCorpus.serialize(root_path+'/data/articles.mm',corpus_tfidf)
        hdp.save(root_path+'/data/hdp.model')
