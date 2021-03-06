import json
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

   # Package data
    new_user = {
        'username': payload['username'],
        'email': payload['email'],
        'name': payload['name'],
        'bio': payload['bio'],
        'pictures': []
    }

    # Response formatting
    status_code = 201
    body = {}

    try:
        # Part 1. Create Cognito entry for this new user
        logger.info('Registering user ({})'.format(new_user['email']))
        response = cognito.admin_create_user(
            UserPoolId='ap-southeast-2_olj1yh7QQ',
            Username=new_user['username'],
            UserAttributes=[
                {
                    'Name': 'email_verified',
                    'Value': 'True'
                },
                {
                    'Name': 'email',
                    'Value': new_user['email']
                }
            ],
            DesiredDeliveryMediums=[
                'EMAIL'
            ]
        )
        
        if response['ResponseMetadata']['HTTPStatusCode'] != 200:
            logger.warn(response['Error']['Message'])
            body['errors'] = [ '(Part 1)' + response['Error']['Message'] ]
            return {
                'statusCode': response['ResponseMetadata']['HTTPStatusCode'],
                'body': json.dumps(body)
            }

        else:
            logger.info('Registered user ({})'.format(new_user['email']))
            # Get userId generated by Cognito
            print(response)

        # Part 2. Set Cognito password for new user
        logger.info('Setting user password ({})'.format(new_user['email']))
        response = cognito.admin_set_user_password(
            UserPoolId='ap-southeast-2_olj1yh7QQ',
            Username=new_user['username'],
            Password=payload['password'],
            Permanent=True
        )
        
        if response['ResponseMetadata']['HTTPStatusCode'] != 200:
            logger.warn(response['Error']['Message'])
            body['errors'] = [ '(Part 2)' + response['Error']['Message'] ]
            return {
                'statusCode': response['ResponseMetadata']['HTTPStatusCode'],
                'body': json.dumps(body)
            }

        else:
            logger.info('Set user password ({})'.format(new_user['email']))

        # Part 3. Create db item
        logger.info('Creating user ({})'.format(new_user['username']))
        response = users_table.put_item(Item=new_user)

        if response['ResponseMetadata']['HTTPStatusCode'] != 200:
            logger.warn(response['Error']['Message'])
            status_code = response['ResponseMetadata']['HTTPStatusCode']
            body['errors'] = [ '(Part 3)' + response['Error']['Message'] ]
        else:
            logger.info('Created user ({})'.format(new_user['username']))

    except ClientError as e:
        logger.warn(e.response['Error']['Message'])
        status_code = e.response['ResponseMetadata']['HTTPStatusCode']
        body['errors'] = [ e.response['Error']['Message'] ]
 
    return {
        'statusCode': status_code,
        'body': json.dumps(body)
    }
