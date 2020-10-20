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
        'username': payload['username'],
        'password': payload['password']
    }

    # Response formatting
    status_code = 200
    body = {}
    
    # Authenticate credentials
    try:
        logger.info('Logging in user ({})'.format(credentials['username']))
        response = cognito.admin_initiate_auth(
            UserPoolId='ap-southeast-2_olj1yh7QQ',
            ClientId='goitvv8flm10r9u185ol5mpqu',
            AuthFlow='ADMIN_NO_SRP_AUTH',
            AuthParameters={
                'USERNAME': credentials['username'],
                'PASSWORD': credentials['password']
            }
        )

        if response['ResponseMetadata']['HTTPStatusCode'] != 200:
            logger.warn(response['Error']['Message'])
            status_code = response['ResponseMetadata']['HTTPStatusCode']
            body['errors'] = [ response['Error']['Message'] ]
        else:
            logger.info('Logged in user ({})'.format(credentials['username']))
            body = response['AuthenticationResult']

    except ClientError as e:
        logger.warn(e.response['Error']['Message'])
        status_code = e.response['ResponseMetadata']['HTTPStatusCode']
        body['errors'] = [ e.response['Error']['Message'] ]

    return {
        'statusCode': status_code,
        'body': json.dumps(body)
    }
