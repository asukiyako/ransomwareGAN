import requests
import pandas as pd
import os
import pyzipper
import time

headers = { 'API-KEY': 'f1599adeb25bd43f7f3fe65bfaa17473983085c82c08b0d8' }

ZIP_PASSWORD = b'infected'
df= pd.read_csv("malware.csv")

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
                zf.close()
                os.remove(completepath+".zip")
        if((i+1)%100==0):
            time.sleep(60)

#done ggs




