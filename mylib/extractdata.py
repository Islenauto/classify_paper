# -*- encoding: UTF-8 -*-
import psycopg2
import psycopg2.extras
import collections

#使用するdbのプロパティ
hostname = "localhost"
db = "paper_rails_development"
name = "Daiki"

class ExtractData:
    def __init__(self):
        sql_cont = "SELECT * FROM contents;"
        sql_arti = "SELECT * FROM articles;"
        sql_arti_info = "SELECT * FROM article_infos;"
        sql_news = "SELECT * FROM newspapers;"
        sql_arti_cont = "SELECT * FROM articles RIGHT OUTER JOIN contents on articles.id = contents.article_id"
        
        self.article_info_dic = self.get_dic_result(sql_arti_info)
        self.newspaper_dic = self.get_dic_result(sql_news)
        # articles,contentsの結合テーブルを辞書化
        self.arti_cont_dic = self.get_dic_result(sql_arti_cont)

    def get_dic_result(self,sql):
        connector = psycopg2.connect(host=hostname, port=5432, dbname=db, user=name)
        cur = connector.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute(sql)
        res = cur.fetchall()
        dict_result = []
        for row in res:
            dict_result.append(dict(row))
        return dict_result


    def get_select_contents(self,newsname,category):
        # 引数で指定した新聞社の対応id
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
    

    def get_news_id(self,name):
        for dic in self.newspaper_dic:
            if dic['name'] == name:
                return dic['id']
