import json
import uuid
import boto3
import logging
from botocore.exceptions import ClientError


# Set up our logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

# Connect to AWS services
dynamodb = boto3.resource('dynamodb')
users_table = dynamodb.Table('fg-users-table')
cognito = boto3.client('cognito-idp')

def lambda_handler(event, context):
   # Request parsing
    payload = json.loads(event['body'])

   # Unpackage data
    credentials = {
        'email': payload['email'],
        'password': payload['password']
    }

    # Response formatting
    status_code = 200
    body = {}
    
    # Authenticate credentials
    try:
        logger.info('Logging in user ({})'.format(credentials['email']))
        response = cognito.admin_initiate_auth(
            UserPoolId='ap-southeast-2_AeuT2xMHY',
            ClientId='7jb1tguk4pfv2iio8d13jaitcq',
            AuthFlow='ADMIN_NO_SRP_AUTH',
            AuthParameters={
                'USERNAME': credentials['email'],
                'PASSWORD': credentials['password']
            }
        )

        if response['ResponseMetadata']['HTTPStatusCode'] != 200:
            logger.warn(response['Error']['Message'])
            status_code = response['ResponseMetadata']['HTTPStatusCode']
            body['errors'] = [ response['Error']['Message'] ]
        else:
            logger.info('Logged in user ({})'.format(credentials['email']))
            body = response['AuthenticationResult']

    except ClientError as e:
        logger.warn(e.response['Error']['Message'])
        status_code = e.response['ResponseMetadata']['HTTPStatusCode']
        body['errors'] = [ e.response['Error']['Message'] ]

    return {
        'statusCode': status_code,
        'body': json.dumps(body)
    }
