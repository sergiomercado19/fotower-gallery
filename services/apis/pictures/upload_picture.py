import json


def lambda_handler(event, context):

    # Response formatting
    body = {
        "message": "Picture uploaded"
    }
    response = {
        "statusCode": 201,
        "body": json.dumps(body)
    }

    return response
