import pymysql

class Test(object):
    def __init__(self):
        self.conn = pymysql.connect(host="106.15.231.105", port=3306, user="root", password="206209", db="researcher")
        self.cursor = self.conn.cursor()

    def select_user(self, user_name: str):
        """
        查询 user_id
        :param user_name:
        :return: user_id
        """
        try:
            # sql = "select user_id from user where name = %s"
            # self.cursor.execute(sql, (user_name,))

            sql = "select user_id from user"
            self.cursor.execute(sql)

            row = self.cursor.fetchone()
            if row == None:
                return -1
            else:
                return row[0]
        except Exception as e:
            print(e)
        finally:
            self.conn.close()




if __name__ == "__main__":
    client = Test()
    print(client.select_user("sdf"))