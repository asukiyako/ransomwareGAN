import requests
import pandas as pd
import os
import pyzipper
import time

headers = { 'API-KEY': 'f1599adeb25bd43f7f3fe65bfaa17473983085c82c08b0d8' }

ZIP_PASSWORD = b'infected'
df= pd.read_csv("sha256_ransomware.csv")


for i in range(len(df)):
    data = {
            'query': 'get_file',
            'sha256_hash': df["SHA256"][i],
        }
    sha256=df["SHA256"][i]
    print("API call: ",i+1,"/",len(df))
  
    try:
        response = requests.post('https://mb-api.abuse.ch/api/v1/', data=data, timeout=30, headers=headers, allow_redirects=True)
    except requests.exceptions.Timeout:
        print("timed out!\n")
        time.sleep(60)
        try:
            response = requests.post('https://mb-api.abuse.ch/api/v1/', data=data, timeout=30, headers=headers, allow_redirects=True)
        except:
            continue
    except requests.exceptions.RequestException as e:
        print("Request failed:", e,"\n")
        time.sleep(60)
        try:
            response = requests.post('https://mb-api.abuse.ch/api/v1/', data=data, timeout=30, headers=headers, allow_redirects=True)
        except:
            continue

    if '<title>502' in response.text:
        time.sleep(60)
        response = requests.post('https://mb-api.abuse.ch/api/v1/', data=data, timeout=30, headers=headers, allow_redirects=True)
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

#done ggs
