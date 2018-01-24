# -*- encoding: UTF-8 -*-
import os,sys
import nltk,pandas,numpy
import treetaggerwrapper as ttw
from itertools import chain
from tqdm import tqdm
from gensim import corpora,models
from mylib.topicmodel import TopicModel
from mylib.ngram import Ngram


class GrantLabel:
    def __init__(self,topicmodel,method):

        self.topic_model = topicmodel
        self.method = method
        self.W_Theta = self.topic_model.W_Theta_indoc # トピック毎の単語生起確率リスト
        self.C = self.topic_model.sentences_parsed # 文脈情報に用いるコーパスC
        self.ngram = Ngram(self.C,n=2) # ngramの言語モデルを作成                        

        #self.labels = self.init_labels(tag_stopwd=['CC','DT','IN','MD','RB'])
        self.labels = set(list(chain.from_iterable(self.ngram.texts_ngram)))
        self.labels_scored = {} # スコアリングしたラベルの辞書をトピック毎に格納する辞書(hashkey=トピック番号)
        self.calc_score_labels(method)


    # ラベル候補を作成(tag_stopwdで指定した品詞を含むラベルは排除)
    def init_labels(self,tag_stopwd):
        
        tagdir = os.getenv('TREETAGGER_ROOT')
        tagger = ttw.TreeTagger(TAGLANG='en',TAGDIR=tagdir)

        labels = set(list(chain.from_iterable(self.ngram.texts_ngram)))
        new_labels = []
        for label in labels:
            pos_results = [result.split('\t')[1] for result in tagger.TagText(' '.join(label))]
            if list(set(pos_results) & set(tag_stopwd)) == []: new_labels.append(label) 
        return new_labels


    def calc_score_label(self,label,id_topic,W_theta):
        
        score = 0      
        # zero-order relevance (normalize:uniform dist)
        if self.method == 0:                
            for word in label:
                score += numpy.log(W_theta[word])
        
        # first-order relevance
        elif self.method == 1:
            label = '-'.join(label)
            for word, w_theta in tqdm(W_theta.items()):
                w_C = self.dic_mle_1gram[word] # コーパスCでの単語wの生起確率(最尤推定量)
                l_C = self.dic_mle_ngram[label] # コーパスCでのラベルlの生起確率(最尤推定量)
                cooccur_wl = self.dic_cooccur[word][label] # w,lの共起頻度
                wl_C = cooccur_wl + 1 / (len(self.W_Theta[id_topic].keys()) - self.ngram.n + 1)
                score += w_theta * numpy.log2(wl_C / (w_C * l_C)) # w_theta * PMI(w,l|C)
                score -= w_theta * numpy.log2(w_theta / w_C) # KLダイバージェンス(トピック-コーパスC)
        
        return score
    
    
    def calc_score_labels(self,method):
        
        if method == 1:
            self.dic_mle_1gram = Ngram(self.C,n=1).mle()
            self.dic_mle_ngram = self.ngram.mle()
            self.dic_cooccur = self.ngram.make_dic_cooccur(self.topic_model.W,self.labels,self.C)

        for id_topic,W_theta in tqdm(self.W_Theta.items()):
            labels_scored_theta = {' '.join(label):self.calc_score_label(label,id_topic,W_theta) for label in tqdm(self.labels)}
            self.labels_scored[id_topic] = labels_scored_theta


    def show_labels(self,id_topic,num_labels=10):
        df = pandas.Series(self.labels_scored[id_topic]).sort_values(ascending=False)
        return (df[:num_labels])
