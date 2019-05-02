import pymysql

HOST = "106.15.231.105"
PORT = 3306
USER = "root"
PASSWORD = "206209"
DB = "researcher"


class MysqlClient(object):

    def __init__(self):
        self._conn = pymysql.connect(host=HOST, port=PORT, user=USER, password=PASSWORD, db=DB)
        self._cursor = self._conn.cursor()

    def select_all_users(self):
        """
        查询所有的用户
        :return: list
        """
        try:
            sql = "select user_id, name from user"
            self._cursor.execute(sql)

            rows = self._cursor.fetchall()
            return rows
        except Exception as e:
            pass

    def update_similarity(self):
        """
        将similarity的学者名改为user_id
        :return: list
        """
        count = 0
        rows = self.select_all_users()
        for row in rows:
            update_f_name_sql = "update similarity set f_name = %s where f_name = %s"
            update_s_name_sql = "update similarity set s_name = %s where s_name = %s"

            try:
                self._cursor.execute(update_f_name_sql, (str(row[0]), row[1]))
                self._conn.commit()

                try:
                    self._cursor.execute(update_s_name_sql, (str(row[0]), row[1]))
                    self._conn.commit()
                    count += 1
                    print("count: {0}".format(count))
                except Exception as e:
                    pass
            except Exception as e:
                pass


    def close(self):
        self._cursor.close()
        self._conn.close()

if __name__ == "__main__":
    client = MysqlClient()
    client.update_similarity()
    client.close()

