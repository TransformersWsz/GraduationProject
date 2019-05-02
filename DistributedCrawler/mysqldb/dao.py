import pymysql

from webcrawler.log import Log

from .setting import *


class MysqlClient(object):

    def __init__(self):
        self.conn = pymysql.connect(host=HOST, port=PORT, user=USER, password=PASSWORD, db=DB)
        self.cursor = self.conn.cursor()

        self.log = Log("dao.log")

    def insert_user(self, user: tuple):
        """
        插入用户信息
        :param user: 用户信息
        :return: user_id
        """
        isExist = self.select_user(user[0])
        if isExist == -1:
            try:
                sql = "INSERT INTO `user` (`name`, `paper`, `citation`, `h_index`, `g_index`, `sociability`, `diversity`, `activity`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                self.cursor.execute(sql, user)
                self.conn.commit()

                self.log.info("{name} 插入成功".format(name=user[0]))
                return self.select_user(user[0])
            except Exception as e:
                self.conn.rollback()

                self.log.error("{name} 插入失败".format(name=user[0]))
                return -1
        else:
            return isExist

    def select_user(self, user_name: str):
        """
        查询 user_id
        :param user_name:
        :return: user_id
        """
        try:
            sql = "select user_id from user where name=%s"
            self.cursor.execute(sql, (user_name,))

            row = self.cursor.fetchone()
            return -1 if row == None else row[0]
        except Exception as e:
            self.log.error("查询名为 {name} 的用户失败。".format(name=user_name))
            return -1

    def select_all_user(self):
        """
        查询所有的用户
        :return: list
        """
        try:
            sql = "select name, paper, citation, h_index, g_index, sociability, diversity, activity from user"
            self.cursor.execute(sql)

            rows = self.cursor.fetchall()
            return rows
        except Exception as e:
            self.log.error("查询所有的用户失败。")
            return []


    def insert_interest(self, interest: tuple):
        """
        插入研究方向
        :param interest: 研究方向
        :return: interest_id
        """
        isExist = self.select_interest(interest[0])
        if isExist == -1:
            try:
                sql = "INSERT INTO `interest` (`name`) VALUES (%s)"
                self.cursor.execute(sql, interest)
                self.conn.commit()

                self.log.info("{name} 插入成功".format(name=interest[0]))
                return self.select_interest(interest[0])
            except Exception as e:
                self.conn.rollback()

                self.log.error("{name} 插入失败".format(name=interest[0]))
                return -1
        else:
            return isExist

    def insert_similarity(self, similarity: tuple):
        """
        插入两个学者的相似度
        :param similarity: (f_name, s_name, distance)
        :return: 1: success 0: failure
        """
        try:
            sql = "insert into similarity VALUES (%s, %s, %s)"
            self.cursor.execute(sql, similarity)
            self.conn.commit()

            return 1
        except Exception as e:
            self.conn.rollback()

            return 0


    def select_interest(self, interest_name: str):
        """
        查询 interest_id
        :param interest_name: 研究方向名称
        :return: interest_id
        """
        sql = "select interest_id from interest where name = %s"
        self.cursor.execute(sql, (interest_name,))

        row = self.cursor.fetchone()
        return -1 if row == None else row[0]

    def insert_user_interest(self, user_interest: tuple):
        """
        插入 user_interest
        :param user_interest: (user_id, interest_id, w)
        :return: 1: success    0: failure
        """
        try:
            sql = "INSERT INTO `user_interest` VALUES (%s, %s, %s)"
            self.cursor.execute(sql, user_interest)
            self.conn.commit()

            self.log.info("{user_id} - {interest_id} - {w} 插入成功".format(user_id=user_interest[0], interest_id=user_interest[1], w=user_interest[2]))
            return 1
        except Exception as e:
            self.conn.rollback()

            self.log.error(
                "{user_id} - {interest_id} - {w} 插入失败".format(user_id=user_interest[0], interest_id=user_interest[1],
                                                              w=user_interest[2]))
            return -1

    def close(self):
        """
        关闭数据库连接
        :return: None
        """
        self.cursor.close()
        self.conn.close()

    def test(self):
        sql = "select * from user"
        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            for row in result:
                print(row[1])
        except Exception as e:
            print(e.args)



