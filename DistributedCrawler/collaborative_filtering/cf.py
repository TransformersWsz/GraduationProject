from webcrawler.log import Log
from mysqldb.dao import MysqlClient


class CF(object):

    def __init__(self):
        self._mysql_client = MysqlClient()
        self._log = Log("cf.log")

    def get_similarity_of_two(self, first_user: tuple, second_user: tuple):
        """
        返回两者之间的相似度
        :param first_user: tuple
        :param second_user: tuple
        :return: tuple
        """
        tuple_length = len(first_user)

        if tuple_length == 0:
            self._log.info("学者数量为0")
            return ()
        else:
            sum = 0.0
            for i in range(tuple_length):
                if i == 0:
                    continue
                else:
                    sum += pow(first_user[i] - second_user[i], 2)
            return (first_user[0], second_user[0], pow(sum, 0.5))


    def insert_to_similarity(self, similarity: tuple):
        """
        插入两个学者的相似度
        :param similarity: (f_name, s_name, distance)
        :return: 1: success 0: failure
        """
        return self._mysql_client.insert_similarity(similarity)

    def calculator(self):
        rows = self._mysql_client.select_all_user()

        length = len(rows)

        i = 0
        while i < length:
            first_user = rows[i]

            j = i+1
            while j < length:
                second_user = rows[j]
                similarity = self.get_similarity_of_two(first_user, second_user)
                res = self.insert_to_similarity(similarity)
                if res == 1:
                    self._log.info("{0}---{1}---{2} 插入成功".format(similarity[0], similarity[1], similarity[2]))
                else:
                    self._log.error("{0}---{1}---{2} 插入失败".format(similarity[0], similarity[1], similarity[2]))

                j += 1

            i += 1

        self._mysql_client.close()

    def test(self):
        self._log.info("wsz")


if __name__ == "__main__":
    cf = CF()
    cf.calculator()