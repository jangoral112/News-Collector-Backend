from dataclasses import dataclass, field


@dataclass
class Feed:
    feed_id: int
    feed_link: str
    keywords: list = field(default_factory=list, init=False)