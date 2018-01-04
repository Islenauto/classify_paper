# -*- encoding: UTF-8 -*-
import os,sys
import nltk,pandas,numpy
from tqdm import tqdm
from gensim import corpora,models
from topicmodel import TopicModel
from datacontroler import DataControler
from ngram import Ngram

class GrantLabel:
    def __init__(self,topicmodel,method):

        data_cont = DataControler()
        self.topic_model = topicmodel
        self.method = method
        self.W_Theta = self.topic_model.W_Theta_indoc # トピック毎の単語生起確率リスト
        self.C = self.topic_model.data_parsed # 文脈情報に用いるコーパスC
        self.ngram = Ngram(self.C,n=2) # ngramの言語モデルを作成                        

        self.labels = list(set(data_cont.flatten_list(self.ngram.texts_ngram)))
        self.labels_scored = {} # スコアリングしたラベルの辞書をトピック毎に格納する辞書(hashkey=トピック番号)
        self.calc_score_labels(method)


    def calc_score_label(self,label,W_theta):
        
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
                cooccur_wl = self.ngram.count_cooccur(word,label,search_window=40,complex_term=True) # w,lの共起頻度
                wl_C = cooccur_wl / (len(self.W_Theta[0].keys()) - self.ngram.n + 1)
                score += w_theta * numpy.log(wl_C + 1 / (w_C * l_C)) # w_theta * PMI(w,l|C)
                score -= w_theta * numpy.log(w_theta / w_C) # KLダイバージェンス(トピック-コーパスC)
        
        return score
    
    
    def calc_score_labels(self,method):
               
        self.dic_mle_1gram = Ngram(self.C,n=1).mle()
        self.dic_mle_ngram = self.ngram.mle()
        for id_topic,W_theta in tqdm(self.W_Theta.items()):
            labels_scored_theta = {' '.join(label):self.calc_score_label(label,W_theta) for label in tqdm(self.labels)}
            self.labels_scored[id_topic] = labels_scored_theta


    def show_labels(self,id_topic,num_labels=10):
        df = pandas.Series(self.labels_scored[id_topic]).sort_values(ascending=False)
        return (df[:num_labels])
