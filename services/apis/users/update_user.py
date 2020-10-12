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
    payload = json.loads(event['body'])
    username = event['pathParameters']['username']

    # Request processing
    email = payload['email'],
    name = payload['name'],
    bio = payload['bio']

    # Response formatting
    status_code = 200
    body = {}

    # Update db item
    try:
        logger.info('Updating user ({})'.format(username))
        response = users_table.update_item(
            Key={
                'username': username
            },
            UpdateExpression="set email=:e, name=:n, bio=:b",
            ExpressionAttributeValues={
                ':e': email,
                ':n': name,
                ':b': bio
            },
            ReturnValues="UPDATED_NEW"
        )

        if response['ResponseMetadata']['HTTPStatusCode'] != 200:
            logger.warn(response['Error']['Message'])
            status_code = response['ResponseMetadata']['HTTPStatusCode']
            body['errors'] = [ response['Error']['Message'] ]
        else:
            logger.info('Updated user ({})'.format(username))

    except ClientError as e:
        logger.warn(e.response['Error']['Message'])
        status_code = e.response['ResponseMetadata']['HTTPStatusCode']
        body['errors'] = [ e.response['Error']['Message'] ]

    
    return {
        'statusCode': status_code,
        'body': json.dumps(body)
    }
