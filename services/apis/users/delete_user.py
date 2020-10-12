import json
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
    username = event['pathParameters']['username']

    # Response formatting
    status_code = 204
    body = {}
    
    # Delete db item
    try:
        logger.info('Deleting user ({})'.format(username))
        response = users_table.delete_item(Key={'username': username})

        if response['ResponseMetadata']['HTTPStatusCode'] != 200:
            logger.warn(response['Error']['Message'])
            status_code = response['ResponseMetadata']['HTTPStatusCode']
            body['errors'] = [ response['Error']['Message'] ]
        else:
            logger.info('Deleted user ({})'.format(username))

    except ClientError as e:
        logger.warn(e.response['Error']['Message'])
        status_code = e.response['ResponseMetadata']['HTTPStatusCode']
        body['errors'] = [ e.response['Error']['Message'] ]

    # Remove Cognito entry for this user

    return {
        'statusCode': status_code,
        'body': json.dumps(body)
    }
