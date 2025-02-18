import requests
import pandas as pd
import os

'''
RIP my initial code 🪦
'''

# def check_sha256(s):
#     if s == "":
#         return
#     if len(s) != 64:
#         raise argparse.ArgumentTypeError("Use sha256 value instead")
#     return str(s)

# parser = argparse.ArgumentParser(description='Download malware sample using the Malware Bazaar API')
# # parser.add_argument('-s', '--hash', help='SHA256 hash of file to download', metavar="HASH", required=True, type=check_sha256)
# parser.add_argument('-s', '--hash', help='SHA256 hash of file to download', metavar="HASH", required=True)
# parser.add_argument('-i', '--info', help='Get info on a malware (does not download)', required=False, default=False, action='store_true')

# args = parser.parse_args()

headers = { 'API-KEY': 'f1599adeb25bd43f7f3fe65bfaa17473983085c82c08b0d8' }

# #Download the malware
# if(args.info == False):
#     data = {
#         'query': 'get_file',
#         'sha256_hash': args.hash,
#     }
#     response = requests.post('https://mb-api.abuse.ch/api/v1/', data=data, timeout=20, headers=headers, allow_redirects=True)
#     if 'file_not_found' in response.text:
#         print("Malware not found")
#         sys.exit()
#     else:
#         open(args.hash+'.zip', 'wb').write(response.content)  
# #Check of malware info
# else:
#     data = {
#         'query': 'get_info',
#         'hash': args.hash,
#     }
#     print(data)
#     response = requests.post('https://mb-api.abuse.ch/api/v1/', data=data, timeout=20, headers=headers)
#     if 'hash_not_found' in response.text:
#         print("Malware not found")
#     else:
#         API_data = response.content.decode("utf-8", "ignore")
#         loc=API_data.find("\"sha256_hash\":")
#         print(API_data[loc+16:loc+64+16])


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
        response = requests.post('https://mb-api.abuse.ch/api/v1/', data=data, timeout=20, headers=headers)
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


#done ggs




