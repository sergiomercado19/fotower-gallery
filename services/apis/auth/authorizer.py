import json
import boto3
import logging
from botocore.exceptions import ClientError


# Set up our logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

# Connect to AWS services
cognito = boto3.client('cognito-idp')

# Based on: https://github.com/mavi888/sam-api-gateway-token-auth/blob/master/authorizer/handler.js

def lambda_handler(event, context):
    # Unpackage data
    token = event.get('authorizationToken', '')
    method_arn = event.get('methodArn', '')
    username = ''

    # Verify token
    try:
        logger.info('Authenticating user')
        response = cognito.get_user(AccessToken=token)

        if response['ResponseMetadata']['HTTPStatusCode'] != 200:
            logger.warn(response['Error']['Message'])
        else:
            logger.info('Authenticated user ({})'.format(response['Username']))
            username = response['Username']

    except ClientError as e:
        logger.warn(e.response['Error']['Message'])

    # Generate response
    if username:
        return generate_auth_response('user', 'Allow', method_arn, username)
    else:
        return generate_auth_response('user', 'Deny', method_arn, username)

def generate_auth_response(principal_id, effect, method_arn, username):
    policy_doc = generate_policy_doc(effect, method_arn)

    return {
        'principalId': principal_id,
        'policyDocument': policy_doc,
        'context': {'username': username}
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
