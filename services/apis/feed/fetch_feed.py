import json


def lambda_handler(event, context):
    
    # Response formatting
    body = {
        "message": "All recent pictures"
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response
