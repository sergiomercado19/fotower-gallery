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
pictures_table = dynamodb.Table('fg-pictures-table')

def lambda_handler(event, context):
    # Request parsing
    request = json.loads(event['body'])

    # Package data
    new_pic = {
        'picId': str(uuid.uuid4()),
        'description': request['description'],
        'location': request['location'],
        'image': request['image']
    }

    # Response formatting
    status_code = 200
    body = {
        'message': ''
    }

    # Insert picture data
    response = ''
    try:
        logger.info('Inserting newly uploaded picture')
        response = response = pictures_table.put_item(Item=new_pic)

        if response['ResponseMetadata']['HTTPStatusCode'] != 200:
            status_code = response['ResponseMetadata']['HTTPStatusCode']
            body['message'] = response['Error']['Message']
            logger.warn(body['message'])
        else:
            body['message'] = 'Picture [{}] inserted'.format(new_pic['picId'])
            logger.info(body['message'])

    except ClientError as e:
        status_code = e.response['ResponseMetadata']['HTTPStatusCode']
        body['message'] = e.response['Error']['Message']
        logger.warn(body['message'])

    # TODO: Link picture to user's account

    return {
        'statusCode': status_code,
        'body': json.dumps(body)
    }
