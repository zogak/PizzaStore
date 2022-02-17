import json, boto3

def lambda_handler(event, context):
    email = event.get("email", None)
    userName = event.get("userName", None)
    age = event.get("age", None)
    
    db = boto3.resource('dynamodb')
    usersTable = db.Table('Users')
    
    try:
        res = usersTable.put_item(
        Item = {
            'email' : email,
            'userName' : userName,
            'age' : age
        })
        return {
            'statusCode' : 200
        }
    except:
        raise Exception(json.dumps({
            'statusCode' : 500,
            'message' : "Internal Server Error"
        }))