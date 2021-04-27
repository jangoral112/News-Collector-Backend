import json
import feedparser
from src.db_connection_config import config
from src.service.accessor import ServiceAccessor

def lambda_handler(event, context):
    accessor = ServiceAccessor(config)
    accessor.feed_service.parse_users_feeds_by_keywords()
        
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
