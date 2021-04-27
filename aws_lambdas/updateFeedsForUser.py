import json
from src.db_connection_config import config
from src.service.accessor import ServiceAccessor


def lambda_handler(event, context):
    accessor = ServiceAccessor(config)
    
    authKey = event['queryStringParameters']['authKey']
    print("AuthKey " + authKey)
    
    body = event['body']
    print("Body" + body)
    feeds_by_website_dict = eval(body)
    
    accessor.feed_service.update_feeds_for_user(authKey, feeds_by_website_dict)
    
    return {
        'statusCode': 200,
        'body': json.dumps("Successfully updated feeds for user")
    }
