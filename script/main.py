# -*- encoding: UTF-8 -*-
import os,sys
root_path = os.path.dirname(os.getcwd())
sys.path.append(root_path+"/mylib/")
import lda 


def main():
    num_topics = sys.argv[1]
    name_news = sys.argv[2]

    model_lda = lda.Lda(num_topics,name_news).lda

    for topic in model_lda.show_topics(-1):
        print (topic)

if __name__=='__main__':
    main()
