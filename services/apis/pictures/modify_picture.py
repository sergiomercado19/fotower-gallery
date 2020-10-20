import json
import time
import boto3
import logging
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key, Attr


# Set up our logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

# Connect to DynamoDB
dynamodb = boto3.resource('dynamodb')
pictures_table = dynamodb.Table('fg-pictures-table')

def lambda_handler(event, context):
    # Request parsing
    payload = json.loads(event['body'])
    # Get username from authorizer
    username = event['requestContext']['authorizer']['username']

    # Request processing
    pic_id = event['pathParameters']['id']
    description = payload['description']
    location = payload['location']

    # Response formatting
    status_code = 200
    body = {}

    # Update db item
    try:
        logger.info('Updating picture ({})'.format(pic_id))
        response = pictures_table.update_item(
            Key={
                'picId': pic_id,
                'owner': username
            },
            UpdateExpression="set modifiedDate=:md, description=:d, location=:l",
            ExpressionAttributeValues={
                ':md': str(time.time()),
                ':d': description,
                ':l': location
            },
            ReturnValues="UPDATED_NEW"
        )

        if response['ResponseMetadata']['HTTPStatusCode'] != 200:
            logger.warn(response['Error']['Message'])
            status_code = response['ResponseMetadata']['HTTPStatusCode']
            body['errors'] = [ response['Error']['Message'] ]
        else:
            logger.info('Updated picture ({})'.format(pic_id))

    except ClientError as e:
        logger.warn(e.response['Error']['Message'])
        status_code = e.response['ResponseMetadata']['HTTPStatusCode']
        body['errors'] = [ e.response['Error']['Message'] ]

    return {
        'statusCode': status_code,
        'body': json.dumps(body)
    }
