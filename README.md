## What this actually is
This code just uses API calls to download Malware samples from Malware Bazaar 
 
We reference a dataset of 21k samples used by someone online but it had only MD5 and SHA1 values
 
So I used the APLI call to get the SHA256 values and then use the SHA256 value to download it
 
API be sus cause it only uses SHA256 to download so it was a pain

### Don't forget to run ``pip install pyzipper``before running the .py script
 
The code also create the folders and downloads samples for you so you dont have to manually classify them :)