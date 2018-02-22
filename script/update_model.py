# -*- encoding: UTF-8 -*-
import os,sys
import pandas as pd
from datetime import date
from mylib.topicmodel import TopicModel
from mylib.database import PaperRails



def input_opr():
    argv = sys.argv

    if(len(argv) < 2):
        print("# 引数が不足しています．新聞社, カテゴリ を指定してください．")
        print("  ex.) BBC science 2016/12/1 2016/12/13")
        quit()
    return (argv[1],argv[2])


def insert_readed_articels(tb_recomm_articles,tb_readed_articles):

    sent_flatten = "\t".join(list(tb_readed_articles["sentence_parsed"]))
    sent_pos_flatten = "\t".join(list(tb_readed_articles["sentence_parsed_with_pos"]))
    tb_temp = pd.DataFrame({"sentence_parsed":sent_flatten,"sentence_parsed_with_pos":sent_pos_flatten},index=[0])
    #tb_inserted = pd.concat([tb_recomm_articles,tb_temp])
    tb_inserted = tb_temp
    return tb_inserted


if __name__=="__main__":
    name,category = input_opr()

    db = PaperRails()
    tb_articles = db.format_tb_articles(db.get_tb_articles(name,category,date(2017,12,1),date(2017,12,31)))
    TopicModel(tb_articles,update=True)
