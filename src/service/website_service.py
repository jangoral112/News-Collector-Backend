from src.service.service import Service
from src.utils.query_creator import QueryCreator
from mysql.connector.errors import Error as SQLError


class WebsiteService(Service):

    def get_website_id_by_name(self, website_name):
        query = QueryCreator.select_where("website_id", "websites", f"website_name LIKE '{website_name}'")
        self._cursor.execute(query)
        result = self._cursor.fetchone()
        if result is None:
            raise Exception(f"Website of name: {website_name} doesn't exist")
        return result['website_id']

    def create_website(self, website_name, website_link):
        query = QueryCreator.insert_into("websites")
        values = (website_name, website_link)
        try:
            self._cursor.execute(query, values)
        except SQLError as e:
            print(f"[{e.sqlstate}] => {e.msg}")
            self._connection.rollback()
        else:
            print("create_website: success")
            self._connection.commit()
