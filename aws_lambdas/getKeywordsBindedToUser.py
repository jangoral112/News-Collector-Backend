import json
from src.db_connection_config import config
from src.service.accessor import ServiceAccessor

def lambda_handler(event, context):
    accessor = ServiceAccessor(config)
    
    authKey = event['queryStringParameters']['authKey']
    
    keywords = accessor.keyword_service.get_keywords_binded_to_user(authKey)
    
    return {
        'statusCode': 200,
        'body': json.dumps(keywords)
    }
