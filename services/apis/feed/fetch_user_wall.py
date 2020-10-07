import json


def lambda_handler(event, context):
    # Request processing
    username = event['pathParameters']['username']

    # Response formatting
    body = {
        "message": "All pictures posted by {}".format(username)
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response
