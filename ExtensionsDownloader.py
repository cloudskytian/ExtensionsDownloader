import json
import os
import re

import requests

edge_download_url = "https://edge.microsoft.com/extensionwebstorebase/v1/crx?response=redirect&x=id%3D{}%26installsource%3Dondemand%26uc"
chrome_download_url = "https://clients2.google.com/service/update2/crx?response=redirect&acceptformat=crx2,crx3&prodversion=9999.0.9999.0&x=id%3D{}%26installsource%3Dondemand%26uc"

with open("extensions.json", "r", encoding="utf-8") as f:
    extensions = json.load(f)

for extension in extensions:
    illegal_chars = r'[\/\\:\*\?"<>|]'
    file_name = re.sub(illegal_chars, " ", extension)
    file_name = ' '.join(file_name.split())
    dir_name = f"Extensions/{file_name}"
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
    if "edge" in extensions[extension]:
        request = requests.get(edge_download_url.format(extensions[extension]["edge"]))
        if request.status_code == 200:
            full_file_name = f"{dir_name}/{file_name}_edge.crx"
            with open(full_file_name, "wb") as f:
                f.write(request.content)
            print(f"{full_file_name} download successful")
        else:
            print(f"{full_file_name} download failed: {request.status_code} | {request.reason}")
    if "chrome" in extensions[extension]:
        request = requests.get(chrome_download_url.format(extensions[extension]["chrome"]))
        if request.status_code == 200:
            full_file_name = f"{dir_name}/{file_name}_chrome.crx"
            with open(full_file_name, "wb") as f:
                f.write(request.content)
            print(f"{full_file_name} download successful")
        else:
            print(f"{full_file_name} download failed: {request.status_code} | {request.reason}")
