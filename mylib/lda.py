# -*- encoding: UTF-8 -*-
from gensim import corpora,models,similarities
import nltk
import treetaggerwrapper as ttw
import re,os
import csv

root_path = os.path.dirname(os.getcwd())

class Lda:
    def __init__(self,num_topics):
        content_dic = self.import_data()
        texts = [dic['sentence'] for dic in content_dic]

        # モデル作成用のdictionary,corpus作成
        dictionary = corpora.Dictionary(texts)
        dictionary.save(root_path+"/data/bbc.dict")
        
        corpus = [dictionary.doc2bow(text) for text in texts]
        corpora.MmCorpus.serialize(root_path+"/data/bcc.mm",corpus)
        #corpus = corpora.MmCorpus('./data/bcc.mm')

        # gensimのldaモデル作成
        lda = models.ldamodel.LdaModel(corpus=corpus, num_topics=num_topics,id2word=dictionary)
        for topic in lda.show_topics(-1):
           print (topic)
        for topic_per_doc in lda[corpus]:
            print (topic_per_doc)


    # csvから辞書データを読み込む
    def import_data(self):
        with open(root_path+"/data/contents.csv","r") as f:
            reader = csv.DictReader(f)
            content_dic = [row for row in reader]
            for dic in content_dic:
                target = dic['sentence']
                dic['sentence'] = re.sub("'|\[|\]","",dic['sentence']).split(',')
            return content_dic


    # 各記事を指定の品詞のみのリストにする
    def stopword(self,texts):
        # tree-taggerのスクリプト本体のpath
        tagdir = os.getenv('TREETAGGER_ROOT')
        tagger = ttw.TreeTagger(TAGLANG='en',TAGDIR=tagdir) 
      
        texts_stopwd = []
        for text in texts:
            # 抽出する品詞リスト
            tag_list = "NP,NPS".split(',')
            results = [res.split('\t') for res in tagger.TagText(text)]

            text_stopwd = [res[2].lower() for res in results if len(res) == 3 and res[1] in tag_list]
            texts_stopwd.append(text_stopwd)
        return texts_stopwd
