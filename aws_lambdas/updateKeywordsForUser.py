import json
from src.db_connection_config import config
from src.service.accessor import ServiceAccessor

def lambda_handler(event, context):
    accessor = ServiceAccessor(config)
    authKey = event['queryStringParameters']['authKey']
    
    body = event['body']
    print("Body" + body)
    
    keywords = eval(body)
    
    accessor.keyword_service.update_keywords_for_user(authKey, keywords)
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
