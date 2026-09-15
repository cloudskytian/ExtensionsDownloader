import json
import os
import re
import shutil
import time
import traceback

import requests

edge_download_url = "https://edge.microsoft.com/extensionwebstorebase/v1/crx?response=redirect&x=id%3D{}%26installsource%3Dondemand%26uc"
chrome_download_url = "https://clients2.google.com/service/update2/crx?response=redirect&acceptformat=crx2,crx3&prodversion=9999.0.9999.0&x=id%3D{}%26installsource%3Dondemand%26uc"


def download_file(url, full_file_name, max_retries=5):
    for attempt in range(1, max_retries + 1):
        try:
            request = requests.get(url.format(extensions[extension]["chrome"]), stream=True, timeout=(10, 60))
            if request.status_code == 200:
                with open(full_file_name, "wb") as f:
                    with open(full_file_name, "wb") as f:
                        for chunk in request.iter_content(chunk_size=64 * 1024):
                            if chunk:
                                f.write(chunk)
                print(f"{attempt}/{max_retries} {full_file_name} download successful")
                return
            else:
                print(f"{attempt}/{max_retries} {full_file_name} download failed: {request.status_code} | {request.reason}")
                if os.path.exists(full_file_name):
                    os.remove(full_file_name)
        except:
            error = Exception(traceback.format_exc())
            print(f"{attempt}/{max_retries} {url} | {error}")
            time.sleep(attempt * 10)


with open("extensions.json", "r", encoding="utf-8") as f:
    extensions = json.load(f)
if not os.path.exists("Extensions"):
    os.makedirs("Extensions")
extensions_names = []
for extension in extensions:
    illegal_chars = r'[\/\\:\*\?"<>|]'
    file_name = re.sub(illegal_chars, " ", extension)
    file_name = ' '.join(file_name.split())
    extensions_names.append(file_name)
    dir_name = f"Extensions/{file_name}"
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
    if "edge" in extensions[extension]:
        request = requests.get(edge_download_url.format(extensions[extension]["edge"]))
        full_file_name = f"{dir_name}/{file_name}_edge.crx"
        if request.status_code == 200:
            with open(full_file_name, "wb") as f:
                f.write(request.content)
            print(f"{full_file_name} download successful")
        else:
            print(f"{full_file_name} download failed: {request.status_code} | {request.reason}")
    if "chrome" in extensions[extension]:
        request = requests.get(chrome_download_url.format(extensions[extension]["chrome"]))
        full_file_name = f"{dir_name}/{file_name}_chrome.crx"
        if request.status_code == 200:
            with open(full_file_name, "wb") as f:
                f.write(request.content)
            print(f"{full_file_name} download successful")
        else:
            print(f"{full_file_name} download failed: {request.status_code} | {request.reason}")
for dir_name in os.listdir("Extensions"):
    if dir_name not in extensions_names:
        shutil.rmtree(f"Extensions/{dir_name}")
