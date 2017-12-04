# -*- encoding: UTF-8 -*-
import os,sys,re
import pandas                                          
import random
root_path = os.path.dirname(os.getcwd())
sys.path.append(root_path+"/mylib/")
import lda,datacontroler as dtct


def main():
    name_news = sys.argv[1]
    category = sys.argv[2]
    num_sample = int(sys.argv[3])

    datacont = dtct.DataControler()
    articles = datacont.import_data(name_news,category)
    num_article = len(articles)
    if num_sample > num_article: num_sample = num_article
    
    ave = 0
    iteration = 50
    for i in range(iteration):
        model_lda = lda.Lda(random.sample(articles,num_sample))   
        df = pandas.DataFrame(model_lda.topics_indoc)
        ave += df.shape[1]
    ave /= iteration

    print ("{0},{1}".format(num_sample,ave))

if __name__=='__main__':
    main()
