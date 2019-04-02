import pymysql

from .setting import *


def read_file(filename: str):
    def decorator(func):
        def wrapper(self, tablename: str):
            if tablename == "interest_person_top10":
                method = self.insert_person_top10

            if tablename == "interest_w_top10":
                method = self.insert_w_top10

            if tablename == "user_h_index":
                method = self.insert_h_index

            with open(filename, "r") as f:
                line = f.readline()
                while line:
                    line_strict = line.rstrip("\n")
                    arr = line_strict.split("--->")
                    method(arr[0], arr[1])
                    line = f.readline()
        return wrapper
    return decorator

class TxtToDB(object):
    def __init__(self):
        """
        初始化数据库连接
        """
        self.conn = pymysql.connect(host=HOST, port=PORT, user=USER, password=PASSWORD, db=DB)
        self.cursor = self.conn.cursor()

    @read_file("myfolder")
    def test(self, s: str):
        print(s)



    @read_file("txt/interest_person_top10.txt")
    def interest_person_top10_to_db(self, tablename: str):
        """
        插入 interest_person_top10 表
        :param tablename: 表名
        :return: None
        """
        pass

    def insert_person_top10(self, name: str, person: str):
        """
        插入 (name, person)
        :param name: interest_name
        :param person:  count of person in the interest
        :return: None
        """
        try:
            count = int(person)
            sql = "insert into `interest_person_top10` values (%s, %s)"
            self.cursor.execute(sql, (name, count))
            self.conn.commit()
            print("{0}--->{1} insert success".format(name, count))
        except Exception as e:
            self.conn.rollback()
            print("{0}--->{1} insert failure".format(name, count))



    @read_file("txt/interest_w_top10.txt")
    def interest_w_top10_to_db(self, tablename: str):
        """
        插入 interest_w_top10 表
        :param tablename: 表名
        :return: None
        """
        pass

    def insert_w_top10(self, name: str, w: str):
        """
        插入 (name, w)
        :param name: interest_name
        :param w: weight
        :return: None
        """
        try:
            weight = int(w)
            sql = "insert into `interest_w_top10` values (%s, %s)"
            self.cursor.execute(sql, (name, weight))
            self.conn.commit()
            print("{0}--->{1} insert success".format(name, weight))
        except Exception as e:
            self.conn.rollback()
            print("{0}--->{1} insert failure".format(name, weight))



    @read_file("txt/user_h_index.txt")
    def user_h_index_to_db(self, tablename: str):
        """
        插入 user_h_index 表
        :param tablename: 表名
        :return: None
        """
        pass

    def insert_h_index(self, user_id: str, h_index: str):
        """
        插入 (user_id, h_index)
        :param user_id: 用户id
        :param h_index: h指数
        :return: None
        """
        try:
            _user_id = int(user_id)
            _h_index = float(h_index)
            sql = "insert into `user_h_index` values (%s, %s)"
            self.cursor.execute(sql, (_user_id, _h_index))
            self.conn.commit()
            print("{0}--->{1} insert success".format(_user_id, _h_index))
        except Exception as e:
            self.conn.rollback()
            print("{0}--->{1} insert failure".format(_user_id, _h_index))

    def close(self):
        """
        关闭数据库连接
        :return: None
        """
        self.cursor.close()
        self.conn.close()