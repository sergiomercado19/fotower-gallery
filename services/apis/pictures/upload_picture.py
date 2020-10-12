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
    payload = json.loads(event['body'])

    # Package data
    new_pic = {
        'picId': str(uuid.uuid4()),
        'description': payload['description'],
        'location': payload['location'],
        'image': payload['image']
    }

    # Response formatting
    status_code = 201
    body = {}

    # Create db item
    try:
        logger.info('Creating picture ({})'.format(new_pic['picId']))
        response = pictures_table.put_item(Item=new_pic)

        if response['ResponseMetadata']['HTTPStatusCode'] != 200:
            logger.warn(response['Error']['Message'])
            status_code = response['ResponseMetadata']['HTTPStatusCode']
            body['errors'] = [ response['Error']['Message'] ]
        else:
            logger.info('Created picture ({})'.format(new_pic['picId']))

    except ClientError as e:
        logger.warn(e.response['Error']['Message'])
        status_code = e.response['ResponseMetadata']['HTTPStatusCode']
        body['errors'] = [ e.response['Error']['Message'] ]

    # TODO: Link picture to user's account

    return {
        'statusCode': status_code,
        'body': json.dumps(body)
    }
