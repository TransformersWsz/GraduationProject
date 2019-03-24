import pymysql

from .setting import *

class MysqlClient(object):
    def __init__(self):
        self.conn = pymysql.connect(host=HOST, port=PORT, user=USER, password=PASSWORD, db=DB)
        self.cursor = self.conn.cursor()

    def test(self):
        sql = "select * from user"
        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            for row in result:
                print(row[1])
        except Exception as e:
            print(e.args)


