import json
from src.db_connection_config import config
from src.service.accessor import ServiceAccessor

def lambda_handler(event, context):
    accessor = ServiceAccessor(config)
    
    feeds_by_website_dict = accessor.feed_service.get_available_feeds_by_website()
    
    return {
        'statusCode': 200,
        'body': json.dumps(feeds_by_website_dict)
    }
