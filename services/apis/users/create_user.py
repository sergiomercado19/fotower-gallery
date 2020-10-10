import json


def lambda_handler(event, context):
    # Request processing
    username = event['body']['username']
    email = event['body']['email']
    password = event['body']['password']
    password_confirmation = event['body']['password_confirmation']
    name = event['body']['name']
    bio = event['body']['bio']
    
    # Response formatting
    body = {
        "message": "Create user {} ({})".format(username, email)
    }
    response = {
        "statusCode": 201,
        "body": json.dumps(body)
    }

    return response
