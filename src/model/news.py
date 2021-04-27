from dataclasses import dataclass, field


@dataclass(repr=True)
class News:
    feed_id: int
    news_title: str
    news_link: str
    news_description: str
    keywords: list = field(default_factory=list, init=False)
    publish_date: str

    def to_tuple(self):
        return self.news_title, self.news_link, self.news_description, self.publish_date
