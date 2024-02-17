import base64
import os
import requests
from dotenv import load_dotenv
import hashlib
# Load environment variables from .env file
load_dotenv()
API_GATEWAY = os.getenv("API_GATEWAY") + '/act5/api/v1'


def get_file_content_base64(file_path):
    """Reads a file and returns its base64 encoded content."""
    try:
        with open(file_path, 'rb') as file:
            file_content_binary = file.read()
            return base64.b64encode(file_content_binary).decode('utf-8')
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return None

def make_api_request(method, endpoint, data=None):
    """Makes an API request and returns the response status code and content."""
    url = f"{API_GATEWAY}/{endpoint}"
    headers = {'Content-Type': 'application/json'}
    try:
        response = requests.request(method, url, headers=headers, json=data)
        response.raise_for_status()
        return response.status_code, response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error making API request: {e}")
        return None, None

def view_files(owner):
    """Views files and shared files for a specific owner."""
    if not owner:
        print("Owner's name cannot be empty.")
        return

    data = {'owner': owner}
    status_code, response = make_api_request('GET', 'view', data)
    if status_code == 200 and response:
        files = response.get('files', [])
        shared_files = response.get('sharefile', [])

        if files:
            print("Files:")
            for file in files:
                print(file['Key'], file['Size'], file['LastModified'], file["owner"])

        if shared_files:
            print("Shared Files:")
            for file in shared_files:
                print(file['Key'], file['Size'], file['LastModified'], file["owner"])
    else:
        print("No files found for this owner.")
def check_download_permission(owner, file_name):
    """Checks if the user has permission to download the file."""
    data = {'owner': owner, 'file_name': file_name}
    status_code, response = make_api_request('GET', 'view', data)
    if status_code == 200 and response:
        files = response.get('files', [])
        shared_files = response.get('sharefile', [])
        if files:
            for file in files:
                if file['Key'] == file_name:
                    return True
        if shared_files:
            for file in shared_files:
                if file['Key'] == file_name:
                    return True
    return False
def upload_file(file_name, owner):
    """Uploads a file to the API."""
    file_path = f"./{file_name}"
    file_content = get_file_content_base64(file_path)

    if not file_content:
        return

    data = {
        'owner': owner,  
        'file_name': file_name,
        'file': file_content
    }

    status_code, _ = make_api_request('PUT', 'put', data)
    if status_code == 200:
        print("File uploaded successfully.")

def download_file(file_name, owner):
    """Downloads a file from the API."""
    data = {'owner': owner, 'file_name': file_name}
    response = make_api_request('GET', 'get', data)

    if not response:
        return
    json_data = response[1]

    # Access the 'file_url' key in the JSON data
    file_url = json_data.get('file_url')
    if file_url:
        print("Downloading file...")
        response = requests.get(file_url)
        with open(file_name, 'wb') as file:
            file.write(response.content)
        print("File downloaded successfully.")
    else:
        print("File not found.")

def share_file(owner,file_name, recipient):
    """Shares a file with another user."""
    data = {'owner': owner, 'filename': file_name, 'shareTo': recipient}
    status_code, _ = make_api_request('POST', 'share', data)
    if status_code == 200:
        print(f"File {file_name} shared with {recipient} successfully.")

def new_user(username, password):
    """Creates a new user with the specified username and password."""\
    
    print(f"Creating a new user => {username}")
    confirm_password = password

    if password != confirm_password:
        print("Passwords do not match.")
        return
    
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    data = {'username': username, 'passwordHash': hashed_password}
    status_code, _ = make_api_request('POST', 'register', data)
    if status_code == 200:
        print(f"User {username} created successfully.")

def login(username, password):
    """Logs in to the application with the specified username and password."""
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    data = {'username': username, 'passwordHash': hashed_password}
    
    status_code, _ = make_api_request('POST', 'login', data)
    if status_code == 200:
        print(f"Logged in as {username}.")

def logout():
    """Logs out from the application."""
    return "BYE"

def main():
    """Handles user interaction in the command-line interface."""
    print("Welcome to myDropbox Application")
    print("============================================")
    print("Available commands:")
    print("  - newuser username password password: Create a new user")
    print("  - login username password: Login to your account")
    print("  - logout: Logout from your account")
    print("  - put filename: Upload a file")
    print("  - view: List your files that you have access to")
    print("  - get filename username: Download a file from specific user owner")
    print("  - share filename recipientUsername: Share a file with another user")
    print("  - quit: Exit the program")
    print("============================================")
    username = None
    while True:
        command = input(">> ")
        split_command = command.split(" ")

        if command == "quit":
            print("============================================")
            break
        elif (split_command[0] == "newuser" and len(split_command) == 4):
            password = split_command[2]
            confirm_password = split_command[3]
            if password != confirm_password:
                print("Passwords do not match.")
                continue
            new_user(split_command[1], password)
        elif (split_command[0] == "login" and len(split_command) == 3):
            login(split_command[1], split_command[2])
            username = split_command[1]
        elif command == "logout":
            logout()
            username = None
        elif (split_command[0] == "put" and len(split_command) == 2):
            if (not username):
                print("Please login first.")
                continue
            upload_file(split_command[1], username)
        elif (split_command[0] == "get" and len(split_command) == 3):
            if (not username):
                print("Please login first.")
                continue
            if (check_download_permission(username, split_command[1])):
                download_file(split_command[1], split_command[2])
            else:
                print("You do not have permission to download this file.")
        elif (split_command[0] == "view"):
            if (not username):
                print("Please login first.")
                continue
            view_files(username)
        elif (split_command[0] == "share" and len(split_command) == 3):
            if (not username):
                print("Please login first.")
                continue
            share_file(username,split_command[1], split_command[2])
        else:
            print("Invalid command. Please try again.")


if __name__ == "__main__":
    main()
