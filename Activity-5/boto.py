# Imports
import json
import boto3

# Comments
# This code was created for a Cloud Computing Class on 2/11/2020.

# Create boto3 clients
s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')


def lambda_handler(event, context):
    # Iterate over S3 bucket contents
    for key in s3.list_objects(Bucket='chulalongkorn1234')['Contents']:
        print(key['Key'])

    # Access DynamoDB table
    table = dynamodb.Table('test')
    response = table.get_item(Key={'username': 'mememe', 'id': '1'})
    item = response.get('Item')
    print(item)

    # Return response
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!'),
    }


# This part is not strictly necessary in a Lambda function,
# but it might be helpful for testing locally:
if __name__ == '__main__':
    lambda_handler(None, None)
