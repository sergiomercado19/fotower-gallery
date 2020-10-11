import json
import boto3
import logging
from botocore.exceptions import ClientError


# Set up our logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

# Connect to DynamoDB
dynamodb = boto3.resource('dynamodb')
pictures_table = dynamodb.Table('fg-pictures-table')

def lambda_handler(event, context):
    # Request parsing
    picId = event['pathParameters']['id']

    # Response formatting
    status_code = 200
    body = {}

    # Read db item
    try:
        logger.info('Reading requested picture')
        response = pictures_table.get_item(Key={'picId': picId})

        if response['ResponseMetadata']['HTTPStatusCode'] != 200:
            status_code = response['ResponseMetadata']['HTTPStatusCode']
            body['message'] = response['Error']['Message']
            logger.warn(body['message'])
        else:
            logger.info('Read requested picture')
            body = response['Item']

    except ClientError as e:
        logger.warn(e.response['Error']['Message'])
        status_code = e.response['ResponseMetadata']['HTTPStatusCode']
        body['errors'] = [ e.response['Error']['Message'] ]

    
    return {
        'statusCode': status_code,
        'body': json.dumps(body)
    }
