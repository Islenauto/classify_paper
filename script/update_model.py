# -*- encoding: UTF-8 -*-
import os,sys
import pandas as pd
from datetime import date
from mylib.topicmodel import TopicModel
from mylib.database import PaperRails


# 入力オペーレションメソッド
def input_opr():
    argv = sys.argv

    if(len(argv) < 2):
        print("# 引数が不足しています．新聞社, カテゴリ を指定してください．")
        print("  ex.) BBC science")
        quit()
    return (argv[1],argv[2])


# 指定した記事テーブル-閲覧済み記事テーブルをマージ
def insert_readed_articels(tb_recomm_articles,tb_read_articles):

    sent_flatten = "\t".join(list(tb_read_articles["sentence_parsed"]))
    sent_pos_flatten = "\t".join(list(tb_read_articles["sentence_parsed_with_pos"]))
    tb_temp = pd.DataFrame({"sentence_parsed":sent_flatten,"sentence_parsed_with_pos":sent_pos_flatten},index=[0])
    tb_inserted = pd.concat([tb_recomm_articles,tb_temp])
    tb_inserted = tb_temp
    return tb_inserted


if __name__=="__main__":
    name,category = input_opr() # name:新聞社, category:カテゴリ名

    db = PaperRails()
    tb_articles = db.format_tb_articles(db.get_tb_articles(name,category,date(2018,2,1),date(2018,2,7)))
    #tb_readed_articles = pd.read_excel("../data/read_articles.xlsx")
    #tb_inserted = insert_read_articels(tb_articles,tb_read_articles)
    TopicModel(tb_articles,update=True)
