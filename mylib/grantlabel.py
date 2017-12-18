# -*- encoding: UTF-8 -*-
import os,sys
import nltk,pandas,numpy
import mylib.topicmodel
from mylib.datacontroler import DataControler

class GrantLabel:
    def __init__(self,topicmodel):

        self.topic_model = topicmodel
        self.C = self.topic_model.data_parsed # 文脈情報に用いるテキストデータ
        self.W_Theta = self.topic_model.W_Theta # トピック毎の単語生起確率リスト
        self.labels = DataControler().flatten_list([list(nltk.bigrams(text)) for text in self.C]) # ラベル候補(bi-gram)
        self.labels_scored = []


    def calc_score_label(self,label,W_theta,method):
        
        score = 0
        # zero-order relevance
        if method == 0:
            for word in label:
                if (word in W_theta.keys()):
                    score += numpy.log(W_theta[word])

        # first-order relevance
        elif method == 1:
            for word in label:
                score += 1

        return score
    
    
    def calc_score_labels(self,method=0):
        
        for W_theta in self.W_Theta:
            labels_scored_at_theta = {' '.join(label):self.calc_score_label(label,W_theta,method) for label in self.labels}
            self.labels_scored.append(labels_scored_at_theta)

