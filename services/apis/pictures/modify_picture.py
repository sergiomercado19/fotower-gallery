import json


def lambda_handler(event, context):
    # Request processing
    pictureId = event['pathParameters']['id']

    
    # Response formatting
    body = {
        "message": "Picture with ID '{}' was modified".format(pictureId)
    }
    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response
