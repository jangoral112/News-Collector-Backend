class Service(object):

    def __init__(self, accessor):
        self._accessor = accessor
        self._cursor = self._accessor.cursor
        self._connection = self._accessor.connection

    @property
    def user_service(self):
        return self._accessor.user_service

    @property
    def keyword_service(self):
        return self._accessor.keyword_service

    @property
    def website_service(self):
        return self._accessor.website_service

    @property
    def news_service(self):
        return self._accessor.news_service

    @property
    def feed_service(self):
        return self._accessor.feed_service
