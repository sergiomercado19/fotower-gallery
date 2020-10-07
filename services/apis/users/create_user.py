import json


def lambda_handler(event, context):
    # Request processing
    username = event['body']['username']
    email = event['body']['email']
    
    # Response formatting
    body = {
        "message": "Create user {} ({})".format(username, email)
    }
    response = {
        "statusCode": 201,
        "body": json.dumps(body)
    }

    return response
