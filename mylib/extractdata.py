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

        self.content_dic = self.get_dic_result(sql_cont)
        self.ariticle_dic = self.get_dic_result(sql_arti)
        self.article_info_dic = self.get_dic_result(sql_arti_info)
        self.newspaper_dic = self.get_dic_result(sql_news)


    def get_dic_result(self,sql):
        connector = psycopg2.connect(host=hostname, port=5432, dbname=db, user=name)
        cur = connector.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute(sql)
        res = cur.fetchall()
        dict_result = []
        for row in res:
            dict_result.append(dict(row))
        return dict_result


    def get_select_contents(self,newsname):
        news_id = self.get_news_id(newsname)
        
        # 指定社のカテゴリ毎の記事数の確認部分
        t_dic = collections.defaultdict(int)
        num_sent = 0
        for a_dic in self.ariticle_dic: 
            if a_dic['newspaper_id'] == news_id:
                t_dic[a_dic['category']] += 1
                num_sent += 1
        print (num_sent,t_dic)
        
        id_lis = [a_dic['id'] for a_dic in self.ariticle_dic if a_dic['newspaper_id'] == news_id]
        select_contents = [c_dic for c_dic in self.content_dic if c_dic['id'] in id_lis]
        return select_contents
    

    def get_news_id(self,name):
        for dic in self.newspaper_dic:
            if dic['name'] == name:
                return dic['id']



