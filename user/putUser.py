import json, boto3
from boto3.dynamodb.conditions import Key

def createExpression(body):
    ret = {"expression": "set ", "values" : {}}
    for key in body:
        item = body.get(key)
        ret['expression'] += "%s=:%s," % (key, key)
        expressionKey = ":" + key
        ret['values'][expressionKey] = item
    return ret
    
def lambda_handler(event, context):
    email = event.get("email", None)
    body = event.get("body", None)
    
    db = boto3.resource('dynamodb')
    usersTable = db.Table('Users')
    
    expression = createExpression(body)
    print(expression)
    res = usersTable.update_item(
        Key = {'email' : email},
        UpdateExpression = expression["expression"][:-1],
        ExpressionAttributeValues = expression["values"]
    )
    return {
        'statusCode' : 200
    }