import json


def lambda_handler(event, context):
    # Request processing
    description = event['body']['description']
    location = event['body']['location']
    image = event['body']['image']

    # Response formatting
    body = {
        "message": "Picture uploaded"
    }
    response = {
        "statusCode": 201,
        "body": json.dumps(body)
    }

    return response
