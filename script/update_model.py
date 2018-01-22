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


if __name__=="__main__":
    name,category = input_opr()

    db = PaperRails()
    tb_articles = db.format_tb_articles(db.get_tb_articles(name,category,date(2016,12,1),date(2016,12,13)))
    TopicModel(tb_articles,update=True)
