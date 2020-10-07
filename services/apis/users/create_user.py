import json


def lambda_handler(event, context):
    # Request processing
    username = event['body']['username']
    email = event['body']['email']
    password = event['body']['password']
    password_confirmation = event['body']['password_confirmation']
    first_name = event['body']['first_name']
    last_name = event['body']['last_name']
    
    # Response formatting
    body = {
        "message": "Create user {} ({})".format(username, email)
    }
    response = {
        "statusCode": 201,
        "body": json.dumps(body)
    }

    return response
