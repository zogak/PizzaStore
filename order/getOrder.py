import json, boto3
from boto3.dynamodb.conditions import Key

def lambda_handler(event, context):
    allOrders = event.get('all', None)
    email = event.get('email', None)
    orderId = event.get('orderId', None)
    
    db = boto3.resource('dynamodb')
    ordersTable = db.Table('Orders')
    
    try:
        if allOrders:
            res = ordersTable.query(
                KeyConditionExpression = Key('email').eq(email)
            )
           
        else:
            if orderId is None:
                raise Exception(json.dumps({
                    'statusCode' : 400,
                    'message' : "Bad Request. orderId required"
                }))
            res = ordersTable.query(
                KeyConditionExpression = Key('email').eq(email) & Key('orderId').eq(orderId)
            )
    
        return {
            'statusCode': 200,
            'body': res['Items']
        }
        
    except:
        raise Exception(json.dumps({
            'statusCode' : 500,
            'message' : "Internal Server Error"
        }))