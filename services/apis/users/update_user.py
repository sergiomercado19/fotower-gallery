import json


def lambda_handler(event, context):
    # Request processing
    username = event['pathParameters']['username']
    
    # Response formatting
    body = {
        "message": "Update {}'s details".format(username)
    }
    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response
