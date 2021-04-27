from src.service.service import Service
from src.utils.query_creator import QueryCreator
from mysql.connector.errors import Error as SQLError


class KeywordService(Service):

    def get_keyword_id_by_value(self, keyword):
        query = QueryCreator.select_where("keyword_id", "keywords", f"keyword_value LIKE '{keyword}'")
        self._cursor.execute(query)
        result = self._cursor.fetchone()
        if result is None:
            raise Exception(f"Keyword of value: {keyword} doesn't exist")
        return result['keyword_id']

    def get_keyword_value_by_id(self, keyword_id):
        query = QueryCreator.select_where("keyword_value", "keywords", f"keyword_id={keyword_id}")
        self._cursor.execute(query)
        result = self._cursor.fetchone()
        if result is None:
            raise Exception(f"Keyword of id: {keyword_id} doesn't exist")
        return result['keyword_value']

    def create_keyword(self, authkey: str, keyword: str):

        try:
            self.__create_keyword_in_keywords(keyword)
        except SQLError as e:
            print(f"[{e.sqlstate}] => {e.msg}")
            self._connection.rollback()
        else:
            print("create_keyword_in_keywords: success")

        try:
            self.__create_keyword_binding_with_user(authkey, keyword)
        except SQLError as e:
            print(f"[{e.sqlstate}] => {e.msg}")
            self._connection.rollback()
        else:
            self._connection.commit()
            print("create_keyword_binding_with_user: success")

    def update_keywords_for_user(self, user_authkey, keywords):
        user_id = self.user_service.get_user_id_by_authkey(user_authkey)
        try:
            query = (f"DELETE FROM users_keywords WHERE user_id = {user_id}")
            self._cursor.execute(query)
        except SQLError as e:
            print(f"[{e.sqlstate}] => {e.msg}")
            self._connection.rollback()
        else:
            self._connection.commit()

        for keyword in keywords:
            self.create_keyword(user_authkey, keyword)


    def get_keywords_binded_to_user(self, user_authkey):
        user_id = self.user_service.get_user_id_by_authkey(user_authkey)

        query = ("SELECT keyword_value FROM keywords "
                 "INNER JOIN users_keywords on keywords.keyword_id = users_keywords.keyword_id "
                 f"WHERE users_keywords.user_id = {user_id}")

        self._cursor.execute(query)
        results = self._cursor.fetchall()
        keywords = [row["keyword_value"] for row in results]

        return keywords

    def __create_keyword_in_keywords(self, keyword):
        query = QueryCreator.insert_into("keywords")
        self._cursor.execute(query, (keyword, ))

    def __create_keyword_binding_with_user(self, authkey, keyword):
        user_id = self.user_service.get_user_id_by_authkey(authkey)
        keyword_id = self.get_keyword_id_by_value(keyword)
        query = QueryCreator.insert_into("users_keywords")
        values = (user_id, keyword_id)
        self._cursor.execute(query, values)
