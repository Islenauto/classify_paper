# -*- encoding: UTF-8 -*-
import treetaggerwrapper as ttw
import nltk
import re,sys,os

root_path = os.path.dirname(os.getcwd())
sys.path.append(root_path+"/mylib/")
import datacontroler as dtct

def preprocess(content_dic,tag_stopwd):
    # ノイズ除去
    texts = [re.sub(r"<br>"," ",dic["sentence"]) for dic in content_dic]
    texts = [re.sub("(\(|\)|(\\r|\\n){1,2}|,|%|These are external links and will open in a new window)","",text) for text in texts]
    texts = [re.sub("([0-9].*?GMT)|(Share\sthis\swith.*?Copy\sthis\slink)","",text) for text in texts]


    # POSによるstopword
    texts_stopwd = stopword(texts,tag_stopwd.split(','))
    for i in range(len(texts_stopwd)):
        content_dic[i]['sentence_preprocessed'] = texts[i]
        content_dic[i]['sentence'] = texts_stopwd[i]
    content_dic = [dic for dic in content_dic if dic['sentence'] != 'DROP']

    return content_dic

def stopword(texts,tag_stopwd):
    # tree-taggerのスクリプト本体のpath
    tagdir = os.getenv('TREETAGGER_ROOT')
    tagger = ttw.TreeTagger(TAGLANG='en',TAGDIR=tagdir)
    
    texts_stopwd = []   
    for text in texts:
        results = [result.split('\t') for result in tagger.TagText(text)]
        # 20単語以下の文書は排除
        if len(results) >= 50:
            text_stopwd = [result[2].lower() for result in results if len(result) == 3 and result[1] in tag_stopwd]
            texts_stopwd.append(text_stopwd)
        else:
            texts_stopwd.append('DROP')
    return texts_stopwd


def main():
    name_news = sys.argv[1]
    category = sys.argv[2]
    

    model_dtct = dtct.DataControler()
    content_dic = model_dtct.get_select_contents(name_news,category)
    content_dic = preprocess(content_dic,"NN,NNS,NP,NPS")
    model_dtct.export_data(content_dic,name_news,category,mode="data")
    
if __name__ == "__main__":
    main()
