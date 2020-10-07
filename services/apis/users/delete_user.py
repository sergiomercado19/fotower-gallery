import json


def lambda_handler(event, context):
    # Request processing
    username = event['pathParameters']['username']
    
    # Response formatting
    body = {
        "message": "User with ID '{}' was deleted".format(username)
    }
    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response
