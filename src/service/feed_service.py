import feedparser

from src.model.feed import Feed
from src.model.news import News
from src.service.service import Service
from mysql.connector.errors import Error as SQLError
from src.utils.query_creator import QueryCreator
from src.parser.dateparser import DateParser
from src.parser.descriptionparser import DescriptionParser

class FeedService(Service):

    def create_feed(self, website_name, feed_name, feed_link):
        website_id = self.website_service.get_website_id_by_name(website_name)
        query = QueryCreator.insert_into("rss_feeds")
        values = (website_id, feed_name, feed_link)
        try:
            self._cursor.execute(query, values)
        except SQLError as e:
            print(f"[{e.sqlstate}] => {e.msg}")
            self._connection.rollback()
        else:
            print("create_feed: success")
            self._connection.commit()

    def bind_user_with_feed(self, user_authkey, feed_id):
        user_id = self.user_service.get_user_id_by_authkey(user_authkey)
        query = QueryCreator.insert_into("users_feeds")
        values = (user_id, feed_id)
        try:
            self._cursor.execute(query, values)
        except SQLError as e:
            print(f"[{e.sqlstate}] => {e.msg}")
            self._connection.rollback()
        else:
            print("bind_user_with_feed: success")
            self._connection.commit()

    def update_feeds_for_user(self, user_authkey, feeds_by_website_dict):

        user_id = self.user_service.get_user_id_by_authkey(user_authkey)

        try:
            query = (f"DELETE FROM users_feeds WHERE user_id = {user_id}")
            self._cursor.execute(query)
        except SQLError as e:
            print(f"[{e.sqlstate}] => {e.msg}")
            self._connection.rollback()
        else:
            self._connection.commit()

        if not feeds_by_website_dict:
            return

        query = ("SELECT rss_feeds.feed_id, feed_name, website_name FROM rss_feeds INNER JOIN websites on rss_feeds.website_id = websites.website_id")
        self._cursor.execute(query)
        feeds_by_website_with_id = self._cursor.fetchall()

        feeds_ids_to_bind = []

        for website, feeds in feeds_by_website_dict.items():
            for feed in feeds:
                for row in feeds_by_website_with_id:
                    if row["website_name"] == website and row["feed_name"] == feed:
                        feeds_ids_to_bind.append(row["feed_id"])
                        break

        self.bind_user_with_many_feeds(user_id, feeds_ids_to_bind)

    def bind_user_with_many_feeds(self, user_id, feeds_ids):

        query = ("INSERT INTO users_feeds (user_id, feed_id) VALUES " + ", ".join(f"({user_id}, {feed_id})" for feed_id in feeds_ids))

        try:
            self._cursor.execute(query)
        except SQLError as e:
            print(f"[{e.sqlstate}] => {e.msg}")
            self._connection.rollback()
        else:
            print("bind_user_with_feeds: success")
            self._connection.commit()


    def parse_users_feeds_by_keywords(self):
        query = (
            "SELECT DISTINCT users_feeds.feed_id, rss_feeds.feed_link,"
            " users_keywords.keyword_id, keyword_value FROM users_feeds"
            " INNER JOIN rss_feeds ON users_feeds.feed_id = rss_feeds.feed_id"
            " INNER JOIN users_keywords ON users_feeds.user_id = users_keywords.user_id"
            " INNER JOIN keywords ON users_keywords.keyword_id = keywords.keyword_id"
        )

        self._cursor.execute(query)

        query_results = self._cursor.fetchall()

        feed_list = self.__create_feed_list_from_query_result(query_results)

        for feed in feed_list:
            news_list = self.fetch_news_from_feed(feed)
            for news in news_list:
                found_keywords = self.find_keywords_in_news(news, feed.keywords)
                if found_keywords:
                    keyword_ids = [ID for (ID, _) in found_keywords]
                    self.news_service.create_news(feed.feed_id, news, keyword_ids)
                    print(f"\t{found_keywords=} on {news.news_link}")

    def __create_feed_list_from_query_result(self, query_result):
        result_feeds = []

        for row in query_result:
            result_feed = None

            for feed in result_feeds:
                if feed.feed_id == row["feed_id"]:
                    result_feed = feed
                    break

            if not result_feed:
                result_feed = Feed(row["feed_id"], row["feed_link"])

            result_feed.keywords.append((row["keyword_id"], row["keyword_value"]))

            if result_feed not in result_feeds:
                result_feeds.append(result_feed)

        return result_feeds

    def fetch_news_from_feed(self, feed):

        feed_parsed = feedparser.parse(feed.feed_link)

        news_list = [News(feed.feed_id,
                          entry["title"],
                          entry["link"],
                          DescriptionParser.parse(entry["summary"]) if "summary" in entry else "No description provided.",
                          DateParser.parse(entry["published_parsed"]) if "published_parsed" in entry
                          else DateParser.now())
                    for entry in feed_parsed.entries if entry["title"]]

        return news_list

    def find_keywords_in_news(self, news, keywords):
        found_keywords = []
        title = news.news_title.lower()
        description = news.news_description.lower()

        # for (keyword_id, keyword) in keywords:
        #     for related_keyword in self.related(keyword):
        #         if related_keyword in title + " " + description:
        #             found_keywords.append((keyword_id, keyword))

        for (keyword_id, keyword) in keywords:
            if keyword.lower() in title + " " + description:
                found_keywords.append((keyword_id, keyword))

        return found_keywords

    def get_available_feeds_by_website(self):
        query = ("SELECT feed_name, website_name FROM rss_feeds INNER JOIN websites on rss_feeds.website_id = websites.website_id")

        self._cursor.execute(query)

        results = self._cursor.fetchall()

        feeds_by_website_dict = {}

        for row in results:
            website_name = row["website_name"]
            feed_name = row["feed_name"]

            if website_name not in feeds_by_website_dict.keys():
                feeds_by_website_dict[website_name] = []

            feeds_by_website_dict[website_name].append(feed_name)

        return feeds_by_website_dict
