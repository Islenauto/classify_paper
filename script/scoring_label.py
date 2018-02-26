# -*- encoding: UTF-8 -*-
import os,sys,re
import pandas as pd
from mylib.database import PaperRails
from mylib.topicmodel import TopicModel
from mylib.grantlabel import GrantLabel

root_path = os.path.dirname(os.getcwd())

def input_opr():
    argv = sys.argv

    if (len(argv) < 2):
        print ("引数が不足しています．下記の例のように入力してください．")
        print ("ex.) scoring_label.py BBC science")
        quit()
    return (argv[1],argv[2])


def insert_read_articles(tb_arti_recomm,tb_arti_read):

    sent = "\t".join(list(tb_arti_read["sentence_parsed"]))
    sent_pos = "\t".join(list(tb_arti_read["sentence_parsed_with_pos"]))
    tb_temp = pd.DataFrame({"sentence_parsed":sent,"sentence_parsed_with_pos":sent_pos},index=[0])
    return pd.concat([tb_arti_recomm,tb_temp])


def main():
    name,category = input_opr()
    tb_articles_recomm = pd.read_excel("../data/articles.xlsx")
    tb_articles_read = pd.read_excel("../data/articles_read.xlsx")
    tb_articles_merged = insert_read_articles(tb_articles_recomm,tb_articles_read)
    
    topic_model = TopicModel(tb_articles_merged)
    grant_label = GrantLabel(topic_model,method=1)
    
    id_topics = topic_model.id_topics_indoc
    for i in id_topics:
        labels_dic = grant_label.show_labels(id_topic=i,num_labels=1000)
        pd.DataFrame(labels_dic).to_csv("{0}/result/labels/2gram/first_order_relevance_2/{1}/topic_{2}.csv".format(root_path,category,i))


if __name__=='__main__':
    main()
