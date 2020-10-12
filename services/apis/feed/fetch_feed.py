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

def last_month():
    seconds_in_day = 86400
    days_in_four_weeks = 28
    return int(time.time() - (seconds_in_day * days_in_four_weeks))

def lambda_handler(event, context):
    # Request parsing
    params = event.get('queryStringParameters', None)
    start_key = params.get('key', None) if params else None

    # Response formatting
    status_code = 200
    body = {}

    # Scan db items
    try:
        logger.info('Scanning feed pictures')

        # Scan parameters
        scan_kwargs = {
            'FilterExpression': Attr('modifiedDate').gte(str(last_month()))
        }
        if start_key:
            scan_kwargs['ExclusiveStartKey'] = start_key

        response = pictures_table.scan(**scan_kwargs)

        if response['ResponseMetadata']['HTTPStatusCode'] != 200:
            logger.warn(response['Error']['Message'])
            status_code = response['ResponseMetadata']['HTTPStatusCode']
            body['errors'] = [ response['Error']['Message'] ]
        else:
            logger.info('Scanned feed pictures')
            body['nextKey'] = response.get('LastEvaluatedKey', None)
            body['items'] = response.get('Items', [])
            body['items'].sort(key=lambda x: x['modifiedDate'], reverse=True)

    except ClientError as e:
        logger.warn(e.response['Error']['Message'])
        status_code = e.response['ResponseMetadata']['HTTPStatusCode']
        body['errors'] = [ e.response['Error']['Message'] ]

    return {
        'statusCode': status_code,
        'body': json.dumps(body)
    }
