import json


def lambda_handler(event, context):
    # Use this code if you don't use the http event with the LAMBDA-PROXY
    # integration
    return {
        "message": "Picture uploaded",
        "event": event
    }
