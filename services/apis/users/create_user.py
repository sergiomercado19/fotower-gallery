import json
import uuid
import boto3
import logging
from botocore.exceptions import ClientError


# Set up our logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

# Connect to DynamoDB
dynamodb = boto3.resource('dynamodb')
users_table = dynamodb.Table('fg-users-table')

def lambda_handler(event, context):
   # Request parsing
    payload = json.loads(event['body'])

   # Package data
    new_user = {
        'username': payload['username'],
        'email': payload['email'],
        'name': payload['name'],
        'bio': payload['bio']
    }

    # Response formatting
    status_code = 201
    body = {}
    
    # Create db item
    try:
        logger.info('Creating user ({})'.format(new_user['username']))
        response = users_table.put_item(Item=new_user)

        if response['ResponseMetadata']['HTTPStatusCode'] != 200:
            logger.warn(response['Error']['Message'])
            status_code = response['ResponseMetadata']['HTTPStatusCode']
            body['errors'] = [ response['Error']['Message'] ]
        else:
            logger.info('Created user ({})'.format(new_user['username']))

    except ClientError as e:
        logger.warn(e.response['Error']['Message'])
        status_code = e.response['ResponseMetadata']['HTTPStatusCode']
        body['errors'] = [ e.response['Error']['Message'] ]

    # Create Cognito entry for this new user

    return {
        'statusCode': status_code,
        'body': json.dumps(body)
    }
