# -*- encoding: UTF-8 -*-
import re,os,sys
import psycopg2
import psycopg2.extras
import collections
import csv

root_path = os.path.dirname(os.getcwd())

#使用するdbのプロパティ
hostname = "localhost"
db = "paper_rails_development"
name = "Daiki"

class DataControler:
    def get_select_contents(self,newsname,category):
        # db内のデータを辞書化
        self.db2dic()
        # 引数で指定した新聞社の対応idを取得
        news_id = self.get_news_id(newsname)

        # 指定社のカテゴリ毎の記事数の確認部分
        num_category_dic = collections.defaultdict(int)
        for dic in self.arti_cont_dic: 
            if dic['newspaper_id'] == news_id:
                num_category_dic[dic['category']] += 1
        print (num_category_dic)
        
        # 指定新聞社・カテゴリの記事を抽出(カテゴリ=allは全カテゴリを均等数抽出)
        if category != '-1':
            select_contents = list(filter(lambda dic:dic['newspaper_id'] == news_id and dic['category'] == category,self.arti_cont_dic))
        else:
            num_least_category = min(num_category_dic.values())
            cont_world = list(filter(lambda dic:dic['category'] == 'world',self.arti_cont_dic))[0:num_least_category+1]
            cont_entame = list(filter(lambda dic:dic['category'] == 'entertainment',self.arti_cont_dic))[0:num_least_category+1]
            cont_sports = list (filter(lambda dic:dic['category'] == 'sports',self.arti_cont_dic))[0:num_least_category+1]
            cont_tech = list(filter(lambda dic:dic['category'] == 'technology',self.arti_cont_dic))[0:num_least_category+1]
            cont_science = list(filter(lambda dic:dic['category'] == 'science',self.arti_cont_dic))[0:num_least_category+1]
            cont_business = list(filter(lambda dic:dic['category'] == 'business',self.arti_cont_dic))[0:num_least_category+1]

            select_contents = cont_world + cont_entame + cont_sports + cont_tech + cont_science + cont_business
            select_contents = list(filter(lambda dic:dic['newspaper_id'] == news_id,select_contents))
        return select_contents  


    def db2dic(self):
        sql_cont = "SELECT * FROM contents;"
        sql_arti = "SELECT * FROM articles;"
        sql_arti_info = "SELECT * FROM article_infos;"
        sql_news = "SELECT * FROM newspapers;"
        sql_arti_cont = "SELECT * FROM articles RIGHT OUTER JOIN contents on articles.id = contents.article_id"
        
        self.article_info_dic = self.exe_sql(sql_arti_info)
        self.newspaper_dic = self.exe_sql(sql_news)
        # articles,contentsの結合テーブルを辞書化
        self.arti_cont_dic = self.exe_sql(sql_arti_cont)


    def exe_sql(self,sql):
        connector = psycopg2.connect(host=hostname, port=5432, dbname=db, user=name)
        cur = connector.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute(sql)
        res = cur.fetchall()
        dict_result = []
        for row in res:
            dict_result.append(dict(row))
        return dict_result


    def get_news_id(self,name):
        for dic in self.newspaper_dic:
            if dic['name'] == name:
                return dic['id']


    # csvから辞書データを読み込む
    def import_data(self,name_news,category):
        with open(root_path+"/data/contents_" + name_news + "_" + category + ".csv","r") as f:
            reader = csv.DictReader(f)
            content_dic = [row for row in reader]
            for dic in content_dic:
                target = dic['sentence']
                dic['sentence'] = list(filter(lambda word: word != '' ,re.sub("[^a-zA-Z0-9,]+","",target).split(",")))
            return content_dic


    def export_data(self,data,name_news,category,mode):
        # 出力ファイル名
        name_file_contents = "contents_" + name_news + "_" + category
        name_file_result = "result_" + name_news + "_" + category

        # 記事データを出力する場合(mode = data)
        if mode == "data":
            header = data[0].keys()
            with open(root_path+"/data/" + name_file_contents + ".csv","w") as f:
                writer = csv.DictWriter(f,header)
                header_row = {k:k for k in header}
                writer.writerow(header_row)
                for row in data:
                    writer.writerow(row) 
        
        # 作成したモデルの結果を出力する場合(mode = result)
        elif mode == "result":
            with open(root_path+"/result/" + name_file_result + ".csv","w") as f:
                writer = csv.writer(f)
                header_row = ["topic_num"]
                writer.writerow(header_row) 
                for row in data:
                    writer.writerow(row)
