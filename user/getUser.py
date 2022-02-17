import json, boto3
from boto3.dynamodb.conditions import Key

def lambda_handler(event, context):
    email = event.get("email", None)
    
    db = boto3.resource('dynamodb')
    usersTable = db.Table('Users')
    
    
    res = usersTable.get_item(
        Key = {'email' : email}    
    )
    return {
        'statusCode': 200,
        'body': res['Item']
    }
    