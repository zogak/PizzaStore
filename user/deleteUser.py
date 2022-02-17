import json, boto3
from boto3.dynamodb.conditions import Key

def lambda_handler(event, context):
    email = event.get("email", None)
    
    db = boto3.resource('dynamodb')
    usersTable = db.Table('Users')
    
    try:
        res = usersTable.delete_item(
            Key = {'email' : email}    
        )
        
        return {
            'statusCode' : 200
        }
    except:
        raise Exception(json.dumps({
            'statusCode' : 500,
            'message' : "Internal Server Error"
        }))