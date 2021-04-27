from src.model.news import News
from src.service.service import Service
from src.utils.query_creator import QueryCreator
from mysql.connector.errors import Error as SQLError


class NewsService(Service):

    def get_news_id(self, news_model: News):
        feed_id = news_model.feed_id
        news_link = news_model.news_link
        query = QueryCreator.select_where("news_id", "news", f"feed_id={feed_id} AND news_link LIKE '{news_link}'")
        self._cursor.execute(query)
        result = self._cursor.fetchone()
        if result is None:
            raise Exception(f"News of link: {news_link} and feed_id: {feed_id} does not exist!")
        return result["news_id"]

    def create_news(self, feed_id, news_model, keyword_ids):
        try:
            self._create_news_in_news_table(feed_id, news_model)
        except SQLError as e:
            print(f"[{e.sqlstate}] => {e.msg}")
            self._connection.rollback()
        else:
            self._connection.commit()

        news_id = self.get_news_id(news_model)
        values = [(news_id, keyword_id) for keyword_id in keyword_ids]
        query = QueryCreator.insert_into("news_keywords")

        try:
            self._cursor.executemany(query, values)
        except SQLError as e:
            print(f"[{e.sqlstate}] => {e.msg}")
            self._connection.rollback()
        else:
            print("create_news: success")
            self._connection.commit()

    def _create_news_in_news_table(self, feed_id, news_model: News):
        query = QueryCreator.insert_into("news")
        values = (feed_id, *news_model.to_tuple())
        self._cursor.execute(query, values)

    def get_news_for_user(self, user_authkey):

        user_query = ("SELECT * "
	            "FROM users "
                "INNER JOIN users_feeds ON users.user_id = users_feeds.user_id "
                "INNER JOIN users_keywords ON users.user_id = users_keywords.user_id "
                f"WHERE users.user_authkey LIKE '{user_authkey}'")

        self._cursor.execute(user_query)
        user_query_results = self._cursor.fetchall()

        relevant_feeds_ids = set()
        relevant_keywords_ids = set()

        for newsResult in user_query_results:
            relevant_feeds_ids.add(newsResult['feed_id'])
            relevant_keywords_ids.add(newsResult['keyword_id'])

        news_query = ("SELECT * " 
                    "FROM news "
                    "INNER JOIN rss_feeds ON news.feed_id = rss_feeds.feed_id "
                    "INNER JOIN websites ON rss_feeds.website_id = websites.website_id "
                    "INNER JOIN news_keywords ON news.news_id = news_keywords.news_id "
                    "INNER JOIN keywords ON news_keywords.keyword_id = keywords.keyword_id "
                    "ORDER BY news.publish_date DESC "
                    "LIMIT 600")

        self._cursor.execute(news_query)
        news_query_results = self._cursor.fetchall()

        relevant_news = self._filter_out_irrelevant_news(news_query_results, relevant_feeds_ids, relevant_keywords_ids)

        processed_news = self._create_processed_news_list(relevant_news)

        return processed_news

    def _filter_out_irrelevant_news(self, news_query_results, relevant_feeds_ids, relevant_keywords_ids):
        relevant_news = []

        for result in news_query_results:
            if result['feed_id'] in relevant_feeds_ids and result['keyword_id'] in relevant_keywords_ids:
                relevant_news.append(result)

        return relevant_news

    def _create_processed_news_list(self, news_list):
        relevant_keys = ["website_name", "feed_name", "news_link", "news_title", "publish_date", "news_description", "keywords_string"]

        merged_news_list = []

        for news in news_list:
            news["keywords_string"] = news.pop("keyword_value")

            found_news_list = list(filter(lambda merged_news: merged_news["news_id"] == news["news_id"], merged_news_list))

            if not found_news_list:
                merged_news_list.append(news)
            else:
                found_news_list[0]["keywords_string"] = found_news_list[0]["keywords_string"] + " " + news["keywords_string"]

        processed_news_list = []

        for news in merged_news_list:
            if not self._is_news_duplicate(news, processed_news_list):
                processed_news = {key: news[key] for key in relevant_keys}
                processed_news_list.append(processed_news)

        for news in processed_news_list:
            news["publish_date"] = str(news["publish_date"])
            if not news["news_title"]:
                processed_news_list.remove(news)

        return processed_news_list

    def _is_news_duplicate(self, news, news_list):
        found_news = list(filter(lambda news_from_list: news_from_list["news_title"] == news["news_title"], news_list))

        if len(found_news) == 0:
            return False

        return True





