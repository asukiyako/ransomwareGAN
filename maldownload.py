import requests
import pandas as pd
import os
import pyzipper

'''
RIP my initial code 🪦
'''



headers = { 'API-KEY': 'f1599adeb25bd43f7f3fe65bfaa17473983085c82c08b0d8' }

ZIP_PASSWORD = b'infected'

'''
The problem with this site and API calls is that it only accepts SHA256
But we have only the MD5 and SHA1 values from the .csv
I wrote this code assuming we know its SHA256 vaule :(

To tackle this imma take the SHA1/MD5 values from all rows, and check if it exists in the malware database.
If it exists, I'll query its SHA256 value and store it in another file.
I will then use this file to automate the download process.
'''


df= pd.read_csv("malware.csv")

#Checkk other script for download
#P.S. run this code if you are bored, I already got the SHA256 values for you in the .txt along with its md5 earier if you wanna check any other data in the other csv

#NVM imma mix both in one so it donwloads as soon as it finds the SHA256 value

#Modifying code to download malware sample in respective folders (easy to classify)

directories = []
for i in df["Category"]:
    directories.append(i)

directories=list(set(directories))
print(directories)

for i in directories:
    try:
        os.mkdir(i)
        print(f"Directory '{i}' created successfully.")
    except FileExistsError:
        print(f"Directory '{i}' already exists.")

with open("sha256.txt","w") as f:
    for i in range(len(df)):
        data = {
                'query': 'get_info',
                'hash': df["md5"][i],
            }
        print("API call: ",i+1,"/21752\n")
        response = requests.post('https://mb-api.abuse.ch/api/v1/', data=data, timeout=30, headers=headers)
        if 'hash_not_found' in response.text:
            print("Malware not found")
        else:
            print("FOUND ONE!!\n")
            API_data = response.content.decode("utf-8", "ignore")
            loc=API_data.find("\"sha256_hash\":")
            sha256=API_data[loc+16:loc+64+16]
            f.write(sha256+", "+df["md5"][i]+", "+df["Category"][i]+"\n")
            data = {
            'query': 'get_file',
            'sha256_hash': sha256,
            }
            response = requests.post('https://mb-api.abuse.ch/api/v1/', data=data, timeout=20, headers=headers, allow_redirects=True)
            if 'file_not_found' in response.text:
                print("Malware not found")
            else:
                completepath = os.path.join(df["Category"][i], sha256+".txt")
                open(completepath+'.zip', 'wb').write(response.content)
            print("Downloaded!!\n")
            with pyzipper.AESZipFile(completepath+".zip") as zf:
                zf.pwd = ZIP_PASSWORD
                sample = zf.extractall(df["Category"][i])  
                print("Sample unzipped\n")
                os.remove(completepath+".zip")

#done ggs




