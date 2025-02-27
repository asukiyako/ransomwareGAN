import os
import zipfile
import json
import gdown
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

# Setup authentication
gauth = GoogleAuth()
gauth.LocalWebserverAuth()
drive = GoogleDrive(gauth)

# Google Drive Folder ID
FOLDER_ID = "1lpQdZ-G2TMG1GYOiv70ZF8Fe9yWfgthY"

# Output Directories
DOWNLOAD_DIR = "downloads"
EXTRACT_DIR = "rant"
PASSWORD = "maraudermap"

os.makedirs(DOWNLOAD_DIR, exist_ok=True)
os.makedirs(EXTRACT_DIR, exist_ok=True)

# Function to get file list from folder
def get_file_list(folder_id):
    file_list = []
    query = f"'{folder_id}' in parents and trashed=false"
    file_list = drive.ListFile({'q': query}).GetList()
    return file_list

# Download files
file_list = get_file_list(FOLDER_ID)
for file in file_list:
    file_title = file['title']
    file_id = file['id']
    file_path = os.path.join(DOWNLOAD_DIR, file_title)

    print(f"Downloading {file_title}...")
    file.GetContentFile(file_path)

# Unzip files with password
for file in os.listdir(DOWNLOAD_DIR):
    if file.endswith(".zip"):
        file_path = os.path.join(DOWNLOAD_DIR, file)
        try:
            with zipfile.ZipFile(file_path, "r") as zip_ref:
                zip_ref.extractall(EXTRACT_DIR, pwd=PASSWORD.encode())
            print(f"Extracted: {file}")
        except zipfile.BadZipFile:
            print(f"Failed to extract: {file} (Bad Zip File)")

print("Download and extraction complete.")
