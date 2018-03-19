# -*- encoding: UTF-8 -*-
import os,sys
import nltk,pandas,numpy
import treetaggerwrapper as ttw
from itertools import chain
from tqdm import tqdm
from operator import itemgetter
from gensim import corpora,models
from mylib.topicmodel import TopicModel
from mylib.ngram import Ngram


class GrantLabel:
    def __init__(self,topicmodel,method):

        self.topic_model = topicmodel # トピックモデル
        self.method = method # ラベルのスコアリング手法
        self.W_Theta = self.topic_model.W_Theta_indoc # トピック毎の単語生起確率リスト
        self.C = self.topic_model.sentences_parsed # 文脈情報に用いるコーパスC
        self.ngram = Ngram(self.C,n=2) # ngramの言語モデルを作成        
        #self.dic_cooccur_wl = pandas.read_csv("../data/cooccur_wl_{0}gram_30(all).csv".format(self.ngram.n),index_col=0,encoding="cp932")
        self.labels = self.make_label(tscore=True,pos=False) # ラベル候補 
        self.labels_scored = {} # スコアリングしたラベルの辞書をトピック毎に格納する辞書(hashkey=トピック番号)
        
        self.calc_score_labels(method) # ラベルのスコアリング(ラベルとトピックの意味的近さのみ考慮)
        self.calc_score_labels_2(self.labels_scored,myu=1.0) (他トピックとの差別化を考慮)
        

    # ラベル候補を作成(品詞とtスコアによる選定)
    def make_label(self,tscore=False,pos=False):
        
        ngram = Ngram(self.topic_model.sentences_parsed_with_pos,n=2)
        labels = set(list(chain.from_iterable(ngram.texts_ngram)))

        if tscore: labels = self.extract_label_by_tscore(labels)
        if pos: labels = self.extract_label_by_pos(labels,lis_pos=["NN","NNS","NP","NPS"])
        labels = [(label[0].split("-")[0],label[1].split("-")[0]) for label in labels]
        
        return labels


    # t値によるラベル選定(threshold_rank:ラベル候補とする閾値)
    def extract_label_by_tscore(self,labels,threshold_rank=1000):
        
        #dic_cooccur = self.ngram.make_dic_cooccur(self.topic_model.W,self.topic_model.W,self.C)
        #pandas.DataFrame(dic_cooccur).to_csv("../data/dic_cooccur_ww.csv")       
        dic_cooccur = pandas.read_csv("../data/dic_cooccur_ww.csv",index_col=0)
        new_labels = []

        for label in labels:
            label_word = [word_pos.split("-")[0] for word_pos in label]
            t_score = self.ngram.t_score(label_word[0],label_word[1],dic_cooccur)
            new_labels.append((label,t_score))
        new_labels.sort(key=itemgetter(1),reverse=True)
        new_labels = [label for label,t in new_labels]

        return new_labels[:threshold_rank]


    # 品詞によるラベル選定(lis_pos:指定する品詞,mode_invert:Trueでlis_posの品詞以外をラベル候補とする)
    def extract_label_by_pos(self,labels,lis_pos,mode_invert=False):

        new_labels = []
        
        for label in labels:
            label_word = [word_pos.split("-")[0] for word_pos in label]
            label_pos = [word_pos.split("-")[1] for word_pos in label]   
            if mode_invert:
                if len(set(lis_pos) & set(label_pos)) == 0: new_labels.append(label)
            else:
                if len(set(lis_pos) | set(label_pos)) == len(lis_pos): new_labels.append(label)
 
        return new_labels


    # calc_score_labelsの補助メソッド
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
                cooccur_wl = self.dic_cooccur_wl[word][label] # w,lの共起頻度
                wl_C = cooccur_wl + 1 / (len(self.W_Theta[id_topic].keys()) - self.ngram.n + 1)
                score += w_theta * numpy.log2(wl_C / (w_C * l_C)) # w_theta * PMI(w,l|C)
                #score -= w_theta * numpy.log2(w_theta / w_C) # KLダイバージェンス(トピック-コーパスC)
        
        return score


    # ラベルのスコアリング(ラベル-トピックの意味的近さのみ考慮)
    def calc_score_labels(self,method):
        
        if method == 1:
            self.dic_mle_1gram = Ngram(self.C,n=1).mle()
            self.dic_mle_ngram = self.ngram.mle()
            labels = ["-".join(label) for label in self.labels]
            #self.dic_cooccur_wl= self.ngram.make_dic_cooccur(self.topic_model.W,labels,self.C,search_window=10,complex_term=True)
            #pandas.DataFrame(self.dic_cooccur_wl).to_csv("../data/cooccur_wl_{0}gram.csv".format(self.ngram.n))

        for id_topic,W_theta in tqdm(self.W_Theta.items()):
            labels_scored_theta = {' '.join(label):self.calc_score_label(label,id_topic,W_theta) for label in tqdm(self.labels)}
            self.labels_scored[id_topic] = labels_scored_theta


    # ラベルのスコアリング(他トピックとの差別化のみ考慮)
    def calc_score_labels_2(self,labels_scored,myu=0.7):
        
        k = self.topic_model.K
        new_labels_scored = {}

        for i in labels_scored.keys():
            temp_labels_scored = {}
            for label,score in labels_scored[i].items():
                Ei_pmi = score # 該当トピックへのラベルスコア
                Ej_pmi = 0
                for j in labels_scored.keys(): Ej_pmi += labels_scored[j][label]
                new_score = (1 + (myu / (k - 1))) * Ei_pmi - (myu / (k - 1)) * Ej_pmi
                temp_labels_scored[label] = new_score
            new_labels_scored[i] = temp_labels_scored
        
        self.labels_scored = new_labels_scored


    # トピックに付与されたラベルの表示メソッド(num_labels:表示するラベル数)
    def show_labels(self,id_topic,num_labels=10):
        df = pandas.Series(self.labels_scored[id_topic]).sort_values(ascending=False)
        return (df[:num_labels])
