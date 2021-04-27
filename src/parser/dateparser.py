from time import strftime
from datetime import datetime


class DateParser(object):

    DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

    @classmethod
    def parse(cls, date):
        return strftime(cls.DATE_FORMAT, date)

    @classmethod
    def now(cls):
        return datetime.now().strftime(cls.DATE_FORMAT)
