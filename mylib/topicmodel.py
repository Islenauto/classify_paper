#-*- encoding: UTF-8 -*-
from gensim import corpora,models,similarities
import nltk,pandas
import treetaggerwrapper as ttw
import re,sys,os

root_path = os.path.dirname(os.getcwd())

class TopicModel:
    def __init__(self,articles):

        self.data_original = [article['sentence_preprocessed'] for article in articles]
        self.data_parsed = [article['sentence'] for article in articles]
        
        # dictionary,corpus,model作成(新規作成時)
        #dictionary,corpus = self.create_tfcorpus(self.data_parsed,self.data_parsed)
        #tfidf = models.TfidfModel(corpus)
        #corpus_tfidf = tfidf[corpus]
        #dictionary.save(root_path+'/data/articles.dict')
        #corpora.MmCorpus.serialize(root_path+'/data/articles.mm',corpus_tfidf)
        #self.lda = models.ldamodel.LdaModel(corpus=corpus_tfidf, num_topics=6,id2word=dictionary)
        #self.hdp = models.hdpmodel.HdpModel(corpus=corpus_tfidf,id2word=dictionary,T=30)
        #self.hdp.save(root_path+'/data/hdp.model')

        # dictionary,corpus,model読み込み(既存のモデル使用時)
        dictionary = corpora.Dictionary.load(root_path+'/data/articles.dict')
        corpus_tfidf = corpora.MmCorpus(root_path+'/data/articles.mm')
        self.hdp = models.hdpmodel.HdpModel.load(root_path+'/data/hdp.model')
 
        self.topics_indoc = [dict(self.hdp[c]) for c in corpus_tfidf] # 各doc内のトピック分布リスト
        self.num_topics_indoc = pandas.DataFrame(self.topics_indoc).shape[1] # トピック数 
        self.id_topics_indoc = list(pandas.DataFrame(self.topics_indoc).columns) # 文書に割り当てがあるトピックのidリスト
        
        temp = [topic for topic in self.hdp.show_topics(num_topics=-1,num_words=len(dictionary),formatted=False)]
        self.W_Theta = {num:{w_theta[0]:w_theta[1] for w_theta in W_theta} for num,W_theta in temp} # トピック毎の各単語の生起確率辞書
        self.W_Theta_indoc = {num:{w_theta[0]:w_theta[1] for w_theta in W_theta} for num,W_theta in temp if num in self.id_topics_indoc} # トピック毎の各単語の生起確率辞書(文書に割り当てがあるもの)


    def create_tfcorpus(self,texts4dic,texts4corpus):
        # 単一文書の場合は多重リスト化(gensimのDictionaryの仕様上単一リストは受け付けない)
        if isinstance(texts4corpus[0],str): texts4corpus = [texts4corpus]
        dic_word2id = corpora.Dictionary(texts4dic)
        corpus_tf = [dic_word2id.doc2bow(text) for text in texts4corpus]
        return (dic_word2id,corpus_tf)
