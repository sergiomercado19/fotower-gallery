import json
import boto3
import logging
from botocore.exceptions import ClientError


# # Set up our logger
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger()

# # Connect to AWS services
# dynamodb = boto3.resource('dynamodb')
# users_table = dynamodb.Table('fg-users-table')
# cognito = boto3.client('cognito-idp')

# Based on: https://github.com/mavi888/sam-api-gateway-token-auth/blob/master/authorizer/handler.js

def lambda_handler(event, context):
    print('Authorizer')
    print(event)

    # Request parsing
    token = event.get('authorizationToken', '')
    method_arn = event.get('methodArn', '')

    if token:
        return generate_auth_response('user', 'Allow', method_arn)
    else:
        return generate_auth_response('user', 'Deny', method_arn)


def generate_auth_response(principal_id, effect, method_arn):
    policy_doc = generate_policy_doc(effect, method_arn)

    return {
        'principalId': principal_id,
        'policyDocument': policy_doc
    }


def generate_policy_doc(effect, method_arn):
    if (not effect or not method_arn):
        return None

    return {
        'Version': '2012-10-17',
        'Statement': [{
            'Action': 'execute-api:Invoke',
            'Effect': effect,
            'Resource': method_arn
        }]
    }
