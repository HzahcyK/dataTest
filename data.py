from django.shortcuts import render
import pymysql
from django.http import JsonResponse

class Database():
    def __init__(self, host, port, user, password, db, charset="utf8"):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.db = db
        self.charset = charset
    def connect(self):
        self.conn = pymysql.connect(host=self.host, port=self.port, user=self.user, password=self.password, db=self.db, charset=self.charset)
        self.cursor = self.conn.cursor()
    def get_all(self, sql, *args):
        try:
            self.connect()
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            return result
        except Exception as e:
            print(e)
        finally:
            self.cursor.close()
            self.conn.close()

    def get_one(self, sql):
        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchone()
            print(result)
        finally:
            self.cursor.close()
            self.conn.close()
        return result
def tai_read_count(start_time, end_time, item):
    db = Database(host="10.10.10.240", port=5432, user="root", password="tF!e5UN?iGMRkB7Z80Ln#O@uCsP^mS", db="dj_analytics")
    params = []
    start_time = start_time
    end_time = end_time
    dp = item
    sql = "select sum(read_count) from views_article where editor like'%%%s%%' and (pub_date between '%s' and '%s');" % (dp, start_time, end_time)
    params.append(start_time)
    params.append(end_time)
    r = db.get_all(sql)
    return r
def county_read_count(start_time, end_time, item):
    db = Database(host="10.10.10.240", port=5432, user="root", password="tF!e5UN?iGMRkB7Z80Ln#O@uCsP^mS", db="dj_analytics")
    start_time = start_time
    end_time = end_time
    county = item
    sql = "select sum(read_count) from views_article where region like '%%%s%%' and (pub_date between '%s' and '%s');" % (county, start_time, end_time)
    r = db.get_all(sql)
    return r

def app_read_count(start_time, end_time, item):
    db = Database(host="10.10.10.240", port=5432, user="root", password="tF!e5UN?iGMRkB7Z80Ln#O@uCsP^mS", db="dj_analytics")
    start_time = start_time
    end_time = end_time
    app_item = item
    sql = "select sum(read_count) from views_article where category='%s' and (pub_date between '%s' and '%s');" % (app_item, start_time, end_time)
    r = db.get_all(sql)
    return r

def read_count(part_tag, start_time, end_time, item):
    db = Database(host="10.10.10.240", port=5432, user="root", password="tF!e5UN?iGMRkB7Z80Ln#O@uCsP^mS", db="dj_analytics")
    start_time = start_time
    end_time = end_time
    part_tag = part_tag
    switcher = {
        1: tai_read_count,
        2: county_read_count,
        3: app_read_count,
    }
    method = switcher.get(part_tag)
    if method:
        method(start_time, end_time, item)

def main():
    part_tag = input("请输入标签：")
    item = input("请输入模块：")
    result = read_count(part_tag, '2020-01-01 00:00:00', '2020-01-10 00:00:00',item)
    print(result)
if __name__ == '__main__':
    main()



