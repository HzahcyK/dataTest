from django.shortcuts import render
import pymysql
from django.http import JsonResponse

class Database():
    def __init__(self, host, port, user, password, db):
        self.conn = pymysql.connect(host=host, port=port, user=user, password=password, db=db)
        self.cursor = self.conn.cursor()

    def get_all(self, sql, *args):
        try:
            self.cursor.execute(sql, args)
            result = self.cursor.fetchall()
        finally:
            self.cursor.close()
            self.conn.close()
        return result

    def get_one(self, sql):
        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchone()
            print(result)
        finally:
            self.cursor.close()
            self.conn.close()
        return result
def caibian_read_count(start_time, end_time):
    db = Database(host="10.10.10.240", port=5432, user="root", password="tF!e5UN?iGMRkB7Z80Ln#O@uCsP^mS", db="dj_analytics")
    params = []
    start_time = start_time
    end_time = end_time
    sql1 = """
    select sum(read_count) from views_article where editor like "%采编部%" and (pub_date between %s and %s);
    """
    params.append(start_time)
    params.append(end_time)
    r1 = db.get_all(sql1, params[0], params[1])
    return r1

def main():
    result = caibian_read_count('2020-01-01 00:00:00', '2020-01-10 00:00:00')
    return result
if __name__ == '__main__':
    main()



