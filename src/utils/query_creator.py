class QueryCreator(object):
    tables = {
        "keywords": "(keyword_value)",
        "news": "(feed_id, news_title, news_link, news_description, publish_date)",
        "news_keywords": "(news_id, keyword_id)",
        "rss_feeds": "(website_id, feed_name, feed_link)",
        "users": "(user_authkey)",
        "users_feeds": "(user_id, feed_id)",
        "users_keywords": "(user_id, keyword_id)",
        "websites": "(website_name, website_link)"
    }

    fields_count = {
        "keywords": 1,
        "news": 5,
        "news_keywords": 2,
        "rss_feeds": 3,
        "users": 1,
        "users_feeds": 2,
        "users_keywords": 2,
        "websites": 2
    }

    @classmethod
    def get_table_fields(cls, table):
        return cls.tables[table]

    @classmethod
    def get_values_placeholders(cls, table):
        count = cls.fields_count[table] - 1
        place_holders = "%s" + ", %s" * count
        return "(" + place_holders + ")"

    @classmethod
    def insert_into(cls, table):
        fields = cls.get_table_fields(table)
        placeholders = cls.get_values_placeholders(table)
        query = f"INSERT INTO {table} {fields} VALUES {placeholders}"
        return query

    @classmethod
    def select(cls, fields, table):
        return f"SELECT {fields} FROM {table}"

    @classmethod
    def select_where(cls, fields, table, condition):
        return f"SELECT {fields} FROM {table} WHERE {condition}"

    @classmethod
    def select_all(cls, table):
        return f"SELECT * FROM {table}"

    @classmethod
    def select_all_where(cls, table, condition):
        return f"SELECT * FROM {table} WHERE {condition}"

    @classmethod
    def delete_all(cls, table):
        return f"DELETE FROM {table}"

    @classmethod
    def delete_where(cls, table, condition):
        return f"DELETE FROM {table} WHERE {condition}"
