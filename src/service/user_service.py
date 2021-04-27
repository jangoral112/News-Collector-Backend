from src.service.service import Service
from mysql.connector.errors import Error as SQLError
from src.utils.query_creator import QueryCreator


class UserService(Service):

    def get_user_id_by_authkey(self, authkey: str):
        query = QueryCreator.select_where("user_id", "users", f"user_authkey LIKE '{authkey}'")
        self._cursor.execute(query)
        result = self._cursor.fetchone()
        if result is None:
            raise Exception(f"User of authkey: {authkey} doesn't exist")
        return result['user_id']

    def create_user(self, authkey: str):
        query = QueryCreator.insert_into("users")
        try:
            self._cursor.execute(query, (authkey, ))
        except SQLError as e:
            print(f"[{e.sqlstate}] => {e.msg}")
            self._connection.rollback()
        else:
            print("create_user: success")
            self._connection.commit()

    # TODO when there is no record to delete, mysql doesn't want to throw an exception?
    def delete_user(self, authkey: str):
        query = QueryCreator.delete_where("users", f"user_authkey LIKE '{authkey}'")
        try:
            self._cursor.execute(query)
        except SQLError as e:
            print(f"[{e.sqlstate}] => {e.msg}")
            self._connection.rollback()
        else:
            print("delete_user: success")
            self._connection.commit()

