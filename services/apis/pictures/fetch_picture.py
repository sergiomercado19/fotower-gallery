import json
import boto3
import logging
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key


# Set up our logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

# Connect to DynamoDB
dynamodb = boto3.resource('dynamodb')
pictures_table = dynamodb.Table('fg-pictures-table')

def lambda_handler(event, context):
    # Request parsing
    pic_id = event['pathParameters']['id']

    # Response formatting
    status_code = 200
    body = {}

    # Read db item
    try:
        logger.info('Reading picture ({})'.format(pic_id))
        response = pictures_table.get_item(Key={'picId': pic_id})

        if response['ResponseMetadata']['HTTPStatusCode'] != 200:
            logger.warn(response['Error']['Message'])
            status_code = response['ResponseMetadata']['HTTPStatusCode']
            body['errors'] = [ response['Error']['Message'] ]
        else:
            logger.info('Read picture ({})'.format(pic_id))
            body = response['Item']

    except ClientError as e:
        logger.warn(e.response['Error']['Message'])
        status_code = e.response['ResponseMetadata']['HTTPStatusCode']
        body['errors'] = [ e.response['Error']['Message'] ]

    return {
        'statusCode': status_code,
        'body': json.dumps(body)
    }
