#-*- encoding: UTF-8 -*-
from gensim import corpora,models,similarities
import nltk
import treetaggerwrapper as ttw
import re,os
import csv

root_path = os.path.dirname(os.getcwd())

class Lda:
    def __init__(self,num_topics,name_news):
        content_dic = self.import_data(name_news)
        texts = [dic['sentence'] for dic in content_dic]

                                                        
        # モデル作成用のdictionary,corpus作成
        dictionary = corpora.Dictionary(texts)
        dictionary.save(root_path+"/data/bbc.dict")
        
        corpus = [dictionary.doc2bow(text) for text in texts]
        tfidf = models.TfidfModel(corpus)
        corpus_tfidf = tfidf[corpus]
        
        #corpora.MmCorpus.serialize(root_path+"/data/bcc.mm",corpus)
        #corpus = corpora.MmCorpus('./data/bcc.mm')

        # gensimのldaモデル作成
        self.lda = models.ldamodel.LdaModel(corpus=corpus_tfidf, num_topics=num_topics,id2word=dictionary)

    # csvから辞書データを読み込む
    def import_data(self,name_news):
        with open(root_path+"/data/contents_" + name_news + ".csv","r") as f:
            reader = csv.DictReader(f)
            content_dic = [row for row in reader]
            for dic in content_dic:
                target = dic['sentence']
                dic['sentence'] = re.sub("'|\[|\]|\s]","",target).split(",")
            return content_dic
