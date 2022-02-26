import json, boto3
import time
from config import *

def lambda_handler(event, context):
    email = event.get("email", None)
    menu = event.get("menu", None)
    
    db = boto3.resource('dynamodb')
    ordersTable = db.Table('Orders')
    
    #order ID
    userId = email.split('@')[0]
    currentUnixTime = time.time()
    orderId = userId + "-" + str(int(currentUnixTime))
    print('orderId:', orderId)
    
    #price
    totalPrice = 0
    pizzaType = menu.get('pizzaType')
    pizzaCount = menu.get('pizzaCount')
    pizzaSize = menu.get('pizzaSize')
    toppings = menu.get('toppings')
    doughEdge = menu.get('doughEdge')
    
    totalPrice += getTotalPrice(pizzaType, pizzaCount, pizzaSize, toppings, doughEdge)
    
    print(totalPrice)
        
    try:
        res = ordersTable.put_item(
        Item = {
            'email' : email,
            'orderId' : orderId,
            'pizzaType' : pizzaType,
            'pizzaCount' : pizzaCount,
            'pizzaSize' : pizzaSize,
            'toppings' : toppings,
            'doughEdge' : doughEdge,
            'totalPrice' : totalPrice
        })
        return {
            'statusCode' : 200
        }
    
    except:
        raise Exception(json.dumps({
            'statusCode' : 500,
            'message' : "Internal Server Error"
        }))
        
def getTotalPrice(pizzaType, pizzaCount, pizzaSize, toppings, doughEdge):
    ret = 0
    if toppings:
        for topping in toppings:
            ret += TOPPING_TYPE[topping]
    ret += (PIZZA_TYPE[pizzaType] + PIZZA_SIZE[pizzaSize] + DOUGH_EDGE[doughEdge])
    ret *= pizzaCount
    return ret