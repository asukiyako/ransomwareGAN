import os
import gdown
import zipfile

# Google Drive Folder ID
folder_id = "1lpQdZ-G2TMG1GYOiv70ZF8Fe9yWfgthY"
download_dir = "downloads"
extract_dir = "ransomboys"
password = "maraudermap"

# Ensure directories exist
os.makedirs(download_dir, exist_ok=True)
os.makedirs(extract_dir, exist_ok=True)

# Get the list of files in the folder
gdown.download_folder(id=folder_id, output=download_dir, quiet=False)


for file in os.listdir(download_dir):
    if file.endswith(".zip"):
        file_path = os.path.join(download_dir, file)
        try:
            with zipfile.ZipFile(file_path, "r") as zip_ref:
                zip_ref.extractall(extract_dir, pwd=password.encode())
            print(f"Extracted: {file}")
        except zipfile.BadZipFile:
            print(f"Failed to extract: {file} (Bad Zip File)")

print("Download and extraction complete.")
