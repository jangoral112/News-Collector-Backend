import json
from src.db_connection_config import config
from src.service.accessor import ServiceAccessor


def lambda_handler(event, context):
    
    authKey = event['queryStringParameters']['authKey']
    
    accessor = ServiceAccessor(config)
    
    try:
        accessor.user_service.get_user_id_by_authkey(authKey)
    except Exception as e:
        accessor.user_service.create_user(authKey)
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
