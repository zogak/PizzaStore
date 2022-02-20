import json, boto3
from boto3.dynamodb.conditions import Key

def lambda_handler(event, context):
    email = event.get("email", None)
    orderId = event.get("orderId", None)
    
    db = boto3.resource('dynamodb')
    ordersTable = db.Table('Orders')
    
    try:
        res = ordersTable.delete_item(
            Key = {
                'email' : email,
                'orderId' : orderId
            }
        )
        
        return {
            'statusCode' : 200
        }
    except:
        raise Exception(json.dumps({
            'statusCode' : 500,
            'message' : "Internal Server Error"
        }))