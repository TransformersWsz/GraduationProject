import pymysql

from dbtofile.setting import *


class Hdfs(object):
    def __init__(self):
        """
        初始化数据库连接
        """
        self.conn = pymysql.connect(host=HOST, port=PORT, user=USER, password=PASSWORD, db=DB)
        self.cursor = self.conn.cursor()

    def db_to_interest_person(self):
        """
        写入文件格式：interest_name:num
        :return: None
        """
        sql = "select name from user_interest join interest on user_interest.interest_id = interest.interest_id;"
        self.cursor.execute(sql)

        rows = self.cursor.fetchall()
        with open("interest_person.txt", "w") as f:
            for row in rows:
                content = "{name}--->1\n".format(name=row[0])
                f.write(content)
                print(content)
        print("write to interest_person.txt complete!!!")


    def db_to_interest_w(self):
        """
        写入文件格式：interest_name:w
        :return: None
        """
        sql = "select name, w from user_interest join interest on user_interest.interest_id = interest.interest_id"
        self.cursor.execute(sql)

        rows = self.cursor.fetchall()
        with open("interest_w.txt", "w") as f:
            for row in rows:
                content = "{name}--->{w}\n".format(name=row[0], w=row[1])
                f.write(content)
                print(content)
        print("write to interest_w.txt complete!!!")

    def db_to_user_h_index(self):
        """
        写入文件格式：user_id:h_index
        :return: None
        """
        sql = "select user_id, h_index from user"
        self.cursor.execute(sql)

        rows = self.cursor.fetchall()
        with open("user_h_index.txt", "w") as f:
            for row in rows:
                content = "{user_id}--->{h_index}\n".format(user_id=row[0], h_index=row[1])
                f.write(content)
                print(content)
        print("write to user_h_index.txt complete!!!")

    def close_db(self):
        """
        关闭数据库连接
        :return: None
        """
        self.cursor.close()
        self.conn.close()

if __name__ == "__main__":
    hdfs = Hdfs()
    hdfs.db_to_interest_person()
    hdfs.close_db()
