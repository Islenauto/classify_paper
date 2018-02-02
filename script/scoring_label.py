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


def main():
    name,category = input_opr()

    topic_model = TopicModel()
    grant_label = GrantLabel(topic_model,method=1)
    
    id_topics = topic_model.id_topics_indoc
    for i in id_topics:
        labels_dic = grant_label.show_labels(id_topic=i,num_labels=1000)
        pd.DataFrame(labels_dic).to_csv("{0}/result/labels/2gram/first_order_relevance/{1}/topic_{2}.csv".format(root_path,category,i))


if __name__=='__main__':
    main()
