from mysqldb.dao import MysqlClient

if __name__ == "__main__":
    cient = MysqlClient()
    print(cient.insert_user(('qwe', 123, 123, 123, 132, 78.3, 6.789, 3.124)))

