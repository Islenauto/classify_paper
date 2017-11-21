# -*- encoding: UTF-8 -*-
import os,sys,re
root_path = os.path.dirname(os.getcwd())
sys.path.append(root_path+"/mylib/")
import lda,datacontroler as dtct


def main():
    num_topics = sys.argv[1]
    name_news = sys.argv[2]
    category = sys.argv[3]

    model_lda = lda.Lda(num_topics,name_news,category)

    result_topics = [topic for topic in model_lda.hdp.show_topics(-1)]
    dtct.DataControler().export_data(result_topics,name_news,category,mode="result")


if __name__=='__main__':
    main()
