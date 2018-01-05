# -*- encoding: UTF-8 -*-
import os,sys,re
import pandas
root_path = os.path.dirname(os.getcwd())
sys.path.append(root_path+"/mylib/")
from topicmodel import TopicModel
from datacontroler import DataControler
from grantlabel import GrantLabel


def input_opr():
    argv = sys.argv

    if (len(argv) < 2):
        print ("引数が不足しています．下記の例のように入力してください．")
        print ("ex.) main.py BBC sports")
        quit()
    return (argv[1],argv[2])


def main():
    name_news,category = input_opr()
    articles = DataControler().import_data(name_news,category)

    topic_model = TopicModel(articles)
    print (root_path)
    grant_label = GrantLabel(topic_model,method=1)
    
    id_topics = topic_model.id_topics_indoc
    for i in id_topics:
        labels_dic = grant_label.show_labels(id_topic=i,num_labels=10)
        pandas.DataFrame(labels_dic).to_csv("{0}/result/labels/{1}/topic_{2}.csv".format(root_path,category,i))


if __name__=='__main__':
    main()
