# a short script to download the Supplemental Crime report in pyhon
import requests
import zipfile

url = "https://www.dropbox.com/s/vwpyz3cfxwmilk5/SHR76_16.csv.zip?dl=1"

print('Downloading File.')
r = requests.get(url, stream=True)
scr_zip_file = 'SHR76_16.csv.zip'
with open(scr_zip_file, 'wb') as f:
    for chunk in r.iter_content(chunk_size=1024):
        if chunk:
            f.write(chunk)
print('Unzipping file.')
with zipfile.ZipFile(scr_zip_file, 'r') as zfile:
    zfile.extractall()
print('Completed script.')
