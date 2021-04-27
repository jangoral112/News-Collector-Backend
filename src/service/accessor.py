import mysql

from src.service.feed_service import FeedService
from src.service.keyword_service import KeywordService
from src.service.news_service import NewsService
from src.service.user_service import UserService
from src.service.website_service import WebsiteService


class ServiceAccessor(object):

    def __init__(self, db_config: dict):
        self._config = db_config
        self._connection = mysql.connector.connect(**self._config)
        self._cursor = self._connection.cursor(dictionary=True, buffered=True)
        self._user_service = UserService(self)
        self._keyword_service = KeywordService(self)
        self._website_service = WebsiteService(self)
        self._news_service = NewsService(self)
        self._feed_service = FeedService(self)

    @property
    def cursor(self):
        return self._cursor

    @property
    def connection(self):
        return self._connection

    @property
    def user_service(self):
        return self._user_service

    @property
    def website_service(self):
        return self._website_service

    @property
    def keyword_service(self):
        return self._keyword_service

    @property
    def news_service(self):
        return self._news_service

    @property
    def feed_service(self):
        return self._feed_service
