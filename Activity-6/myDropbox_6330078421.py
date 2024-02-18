import boto3
import json
import base64
import os
from datetime import datetime
from boto3.dynamodb.conditions import Key
import uuid

BASE_PATH = '/act5/api/v1'
GET_PATH = f'{BASE_PATH}/get'
PUT_PATH = f'{BASE_PATH}/put'
VIEW_PATH = f'{BASE_PATH}/view'
REGISTER_PATH = f'{BASE_PATH}/register'
LOGIN_PATH = f'{BASE_PATH}/login'
SHARE_PATH = f'{BASE_PATH}/share'
BUCKET_NAME = os.environ['s3_bucket_name']


def _get_object_key(owner, file_name):
    """Constructs the object key for a file based on owner and name."""
    return f"{owner}/{file_name}"


def list_files_shared_with_user(username):
    dynamo = boto3.resource('dynamodb')
    files = []
    table = dynamo.Table('myDropboxShares')
    response = table.scan(
        FilterExpression=Key('shareTo').eq(username)
    )
    for item in response['Items']:
        files.append(item)
    return files

def convert_sharefile_to_list_files(sharefile):
    s3 = boto3.client('s3')
    file_list=[]
    for data in sharefile:
        file_owner = data['username']
        filename = data['filename']
        content = s3.head_object(Bucket = BUCKET_NAME, Key = file_owner + "/" + filename)
        file_size = content["ContentLength"]
        last_modified = content["LastModified"].strftime("%Y-%m-%d %H:%M:%S")
        file_list.append({
            "Key": filename,
            "Size": file_size,
            "LastModified": last_modified,
            "owner": file_owner
        })
    return file_list
def list_files_for_owner(owner):
    s3 = boto3.client('s3')
    files = []
    prefix = f"{owner}/"  # Assuming folder names are based on owners
    
    response = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix=prefix)
    for obj in response.get('Contents', []):
        dateTime = obj['LastModified']
        stringTime = dateTime.strftime('%Y-%m-%d %H:%M:%S')
        files.append({
            "Key":obj['Key'].split('/')[-1], 
            "Size": obj['Size'], 
            "LastModified": stringTime,
            "owner": owner
        })
    return files[1:]




def get_file_url(owner, file_name):
    """Generates a presigned URL for downloading a file."""
    file_key = _get_object_key(owner, file_name)
    s3 = boto3.client('s3')
    
    file_key = f'{owner}/{file_name}'
    try:
        file_url = s3.generate_presigned_url('get_object', Params={'Bucket': BUCKET_NAME, 'Key': file_key}, ExpiresIn=3600)
        return file_url
    except Exception as e:
        print(f"Error generating URL for {file_key}: {e}")
        return None



def create_folder(folder_path):
    """Creates a folder in the bucket, ignoring errors if it already exists."""
    s3 = boto3.client('s3')
    try:
        s3.put_object(Bucket=BUCKET_NAME, Key=folder_path)
    except Exception as e:
        print(f"Error creating folder {folder_path}: {e}")


def upload_file_to_s3(file_content, file_key):
    """Uploads a file to S3 with the specified key."""
    s3 = boto3.client('s3')
    try:
        s3.put_object(Body=file_content, Bucket=BUCKET_NAME, Key=file_key)
    except Exception as e:
        print(f"Error uploading file {file_key}: {e}")

def register_user(username, passwordHash):
    """Registers a new user in the database."""
    dynamo = boto3.resource('dynamodb')
    try:
        table = dynamo.Table('myDropboxUsers')
        response = table.put_item(
        Item={
            'username': username,
            'password': passwordHash
        },
    )
        return True
    except Exception as e:
        return f"Failed to register user {username, e}. User already exists."
    
      
def login_user(username, password):
  
    # Instantiate a table resource object
    dynamo = boto3.resource('dynamodb')
    table = dynamo.Table('myDropboxUsers')
    
    # Get the user from the database
    response = table.get_item(Key={'username': username})

    # Check if user exists and password matches
    if 'Item' in response:
        user = response['Item']
        if user['password'] == password:
            print("Login successful")
            return True
        else:
            print("Incorrect password")
            return False
    else:
        print("User does not exist")
        return False
    
def sharefile(owner, filename, shareTo):
    share_id = str(uuid.uuid4())
    dynamo = boto3.resource('dynamodb')
    table = dynamo.Table('myDropboxShares')
    try:
        response = table.put_item(
        Item={
            'shareId': share_id,
            'shareFrom': owner,
            'filename': filename,
            'shareTo': shareTo
        },
     )
        return response
    except Exception as e:
        return f"Failed to share file {filename, e}."    
def lambda_handler(event, context):
    """Handles API requests for file operations."""
    try:
        path = event['path']
        body = json.loads(event["body"])

        if path == PUT_PATH:
            return _handle_put_request(body)
        elif path == GET_PATH:
            return _handle_get_request(body)
        elif path == VIEW_PATH:
            return _handle_view_request(body)
        elif path == REGISTER_PATH:
            return _handle_register_request(body)
        elif path == LOGIN_PATH:
            return _handle_login_request(body)
        elif path == SHARE_PATH:
            return _handle_share_request(body)
        else:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Invalid path'})
            }
    except Exception as e:
        print(f"Error handling lambda request: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Internal server error'})
        }


def _handle_put_request(body):
    """Handles PUT requests for uploading files."""
    try:
        owner = body.get('owner')
        file_name = body.get('file_name')
        file = body.get('file')

        if not all([owner, file_name, file]):
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Missing required fields'})
            }

        folder_path = _get_object_key(owner, '')
        create_folder(folder_path)

        file_content = base64.b64decode(file)
        file_key = _get_object_key(owner, file_name)
        upload_file_to_s3(file_content, file_key)

        return {
            'statusCode': 200,
            'body': json.dumps({'post': 'OK'})
        }
    except Exception as e:
        print(f"Error handling PUT request: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Error handling PUT request'})
        }


def _handle_get_request(body):
    """Handles GET requests for download file URLs."""
    try:
        file_name = body.get('file_name')
        owner = body.get('owner')

        if not all([file_name, owner]):
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Missing required fields'})
            }

        file_url = get_file_url(owner, file_name)
        if file_url:
            return {
                'statusCode': 200,
                'body': json.dumps({'file_url': file_url})
            }
        else:
            return {
                'statusCode': 404,
                'body': json.dumps({'error': file_url})
            }
    except Exception as e:
        print(f"Error handling GET request: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Error handling GET request'})
        }


def _handle_view_request(body):
    """Handles VIEW requests for listing files for an owner."""
    try:
        owner = body.get('owner')

        if not owner:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Missing owner field'})
            }

        files = list_files_for_owner(owner)
        sharefile = list_files_shared_with_user(owner)
        file_lists = convert_sharefile_to_list_files(sharefile)
        return {
            'statusCode': 200,
            'body': json.dumps({'files': files, 'sharefile': file_lists})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Error handling VIEW request'})
        }



def _handle_register_request(body):
    """Handles REGISTER requests for creating a new user."""
    try:
        username = body.get('username')
        passwordHash = body.get('passwordHash')
        if not all([username, passwordHash]):
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Missing required fields'})
            }

        response = register_user(username, passwordHash)
        return {
            'statusCode': 200,
            'body': json.dumps({'register': "OK"})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Error handling REGISTER request'})
        }

def _handle_login_request(body):
    """Handles LOGIN requests for logging in a user."""
    try:
        username = body.get('username')
        passwordHash = body.get('passwordHash')
        
        if not all([username, passwordHash]):
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Missing required fields'})
            }

        # Implement login and session management
        response = login_user(username, passwordHash)
        if response:
            return {
                'statusCode': 200,
                'body': json.dumps({'login': 'OK'})
            }
        else:
            return {
                'statusCode': 401,
                'body': json.dumps({'error': 'Invalid credentials'})
            }
    except Exception as e:
        print(f"Error handling LOGIN request: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Error handling LOGIN request'})
        }

def _handle_share_request(body):
    """Handles SHARE requests for sharing a file with another user."""
    try:
        owner = body.get('owner')
        filename = body.get('filename')
        shareTo = body.get('shareTo')

        if not all([owner, filename, shareTo]):
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Missing required fields'})
            }

        # Implement sharing logic
        if (owner == shareTo):
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Cannot share with yourself'})
            }
        try:
            sharefile(owner, filename, shareTo)
            return {
                'statusCode': 200,
                'body': json.dumps({'share': 'OK'})
            }
        except Exception as e:
            return {
                'statusCode': 500,
                'body': json.dumps({'error': f'Error sharing file {e}'})
            }
    except Exception as e:
        print(f"Error handling SHARE request: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Error handling SHARE request'})
        }