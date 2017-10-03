# -*- encoding: UTF-8 -*-
import os,sys

root_path = os.path.dirname(os.getcwd())
sys.path.append(root_path+"/mylib/")
import lda 


def main():
    num_topics = sys.argv[1]
    model_lda = lda.Lda(num_topics) 

if __name__=='__main__':
    main()
