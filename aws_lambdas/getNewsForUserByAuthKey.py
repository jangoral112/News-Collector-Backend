import json
from src.db_connection_config import config
from src.service.accessor import ServiceAccessor

def lambda_handler(event, context):
    authKey = event['queryStringParameters']['authKey']
    accessor = ServiceAccessor(config)
    result = accessor.news_service.get_news_for_user(authKey)
    
    response = {}
    response['statusCode'] = 200
    response['headers'] = {}
    response['headers']['Content-Type'] = 'application/json'
    response['body'] = json.dumps(result)
    
    return response
