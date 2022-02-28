import json, boto3
from boto3.dynamodb.conditions import Key
from config import *

def createExpression(body):
    ret = {"expression": "set ", "values" : {}}
    for key in body:
        item = body.get(key)
        ret['expression'] += "%s=:%s," % (key, key)
        expressionKey = ":" + key
        ret['values'][expressionKey] = item
    return ret
    
def getTotalPrice(pizzaType, pizzaCount, pizzaSize, toppings, doughEdge):
    ret = 0
    if toppings:
        for topping in toppings:
            ret += TOPPING_TYPE[topping]
    ret += (PIZZA_TYPE[pizzaType] + PIZZA_SIZE[pizzaSize] + DOUGH_EDGE[doughEdge])
    ret *= pizzaCount
    return ret
    
def lambda_handler(event, context):
    email = event.get('email', None)
    orderId = event.get('orderId', None)
    body = event.get('body', None)
    
    db = boto3.resource('dynamodb')
    ordersTable = db.Table('Orders')
    
    pizzaType = body.get('pizzaType', None)
    pizzaCount = body.get('pizzaCount', None)
    pizzaSize = body.get('pizzaSize', None)
    toppings = body.get('toppings', None)
    doughEdge = body.get('doughEdge', None)
    
    totalPrice = getTotalPrice(pizzaType, pizzaCount, pizzaSize, toppings, doughEdge)
    body['totalPrice'] = totalPrice
    
    expression = createExpression(body)
    print(expression)
    res = ordersTable.update_item(
        Key = {
            'email' : email,
            'orderId' : orderId
            },
        UpdateExpression = expression["expression"][:-1],
        ExpressionAttributeValues = expression["values"]
    )
    return {
        'statusCode' : 200
    }