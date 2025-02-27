

import os
import zipfile

# Define the directory containing the .zip files
directory = '/home/rw/Ransomware'

# Define the password
password = 'maraudermap'

# Iterate over all files in the directory
for filename in os.listdir(directory):
    if filename.endswith('.zip'):
        # Construct the full file path
        file_path = os.path.join(directory, filename)
        
        # Open the zip file
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            try:
                # Extract all contents of the zip file using the password
                zip_ref.extractall(path=directory, pwd=password.encode('utf-8'))
                print(f'Successfully extracted {filename}')
            except RuntimeError as e:
                print(f'Failed to extract {filename}: {e}')
            except zipfile.BadZipFile:
                print(f'{filename} is not a valid zip file.')
            except zipfile.LargeZipFile:
                print(f'{filename} is too large to be extracted.')
            except Exception as e:
                print(f'An error occurred while extracting {filename}: {e}')

print('Extraction complete.')
