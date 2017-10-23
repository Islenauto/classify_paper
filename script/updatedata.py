# -*- encoding: UTF-8 -*-
import treetaggerwrapper as ttw
import nltk
import csv
import sys,os
import re

root_path = os.path.dirname(os.getcwd())
sys.path.append(root_path+"/mylib/")
import extractdata as extdt

def preprocess(content_dic,tag_stopwd):
    # ノイズ除去
    texts = [re.sub(r"<br>"," ",dic["sentence"]) for dic in content_dic]
    texts = [re.sub("(\(|\)|(\\r|\\n){1,2}|,|%)","",text) for text in texts]
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


# dbから抽出したデータをcsvへ出力
def export_data(content_dic,name_news):
    # csvのヘッダ
    header = content_dic[0].keys()
    # 出力ファイル名
    name_file = "contents_" + name_news


    with open(root_path+"/data/" + name_file + ".csv","w") as f:
        writer = csv.DictWriter(f,header)
        header_row = {k:k for k in header}
        writer.writerow(header_row)

        for row in content_dic:
            writer.writerow(row)


def main():
    name_news = sys.argv[1]
    category = sys.argv[2]

    total_dic = extdt.ExtractData()
    content_dic = total_dic.get_select_contents(name_news,category)
    content_dic = preprocess(content_dic,"NN,NNS,NP,NPS")
    export_data(content_dic,name_news)

if __name__ == "__main__":
    main()
