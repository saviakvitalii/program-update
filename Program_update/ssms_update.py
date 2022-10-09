import requests
from datetime import date
from os.path import abspath, dirname, join
from bs4 import BeautifulSoup
import urllib.request
import os
import shutil
import subprocess
import ssl
import time
import wget
###########################

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    # Legacy Python that doesn't verify HTTPS certificates by default
    pass
else:
    # Handle target environment that doesn't support HTTPS verification
    ssl._create_default_https_context = _create_unverified_https_context

headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '\
           'AppleWebKit/537.36 (KHTML, like Gecko) '\
           'Chrome/75.0.3770.80 Safari/537.36'}

###########################
# Basik dir, where script execute
BASE_DIR = dirname(dirname(abspath(__file__)))

#This url adress need change
URL_SITE = 'https://docs.microsoft.com/en-us/sql/ssms/download-sql-server-management-studio-ssms?view=sql-server-ver16'
URL_DOWNLOAD = 'https://learn.microsoft.com/en-us/sql/ssms/release-notes-ssms?view=sql-server-ver16'

#Fuction for get current date
def get_current_date():
    current_date = date.today()
    return current_date

# Function for get old version program
def check_old_version():
    old_version = subprocess.check_output(['powershell.exe',"(Get-Item \"C:\Program Files (x86)\Microsoft SQL Server Management Studio 18\Common7\IDE\SSms.exe\").VersionInfo.ProductVersion"], universal_newlines=True)
    return old_version.replace('.','').replace(' ','').replace(',','')

# Function for get new version program
def check_new_version():
    httpx = requests.get(URL_SITE, headers=headers)
    html = httpx.text
    soup = BeautifulSoup(html, 'html.parser')
    urls = []
    for lines in soup.find_all("ul"):
        urls.append(lines.find_all("li"))
    build_version = str(urls[1])
    new_version = build_version.split()[5][0:-6]
    return new_version.replace('.','').replace(' ','').replace(',','')
  
# Function for compare new and old version
def comparisons_version():
    old_version = int(check_old_version())
    new_version = int(check_new_version())
    if (new_version - old_version) == 0:
        return True
    else:
        return False

# Function for get download file from website and install it
def get_download_and_install_file():
    file = open(rf"{BASE_DIR}\Logs\Result-Ssms-{get_current_date()}.txt", "w")
    if(os.path.exists(f"{BASE_DIR}\\downloads")):
        shutil.rmtree(f"{BASE_DIR}\\downloads")
    os.mkdir(f"{BASE_DIR}\\downloads")
    httpx = requests.get(URL_DOWNLOAD, headers=headers)
    html = httpx.text
    soup = BeautifulSoup(html, 'html.parser')
    result = soup.find_all("a", string="Russian")
    urls = []
    for link in result:
        urls.append(link.get('href'))
    file.write("Downloading...") 
    wget.download(urls[0], f"{BASE_DIR}\\downloads\\ssms_new.exe")
    file.write("\tSUCCESS\n")
    file.write("Installing...")
    process = subprocess.Popen([f'{BASE_DIR}\\downloads\\ssms_new.exe', '/install', '/quiet', '/norestart'])
    process.wait()
    file.write("\tSUCCESS\n")
    time.sleep(100)
    os.remove(f"{BASE_DIR}\\downloads\\ssms_new.exe")
    shutil.rmtree(f"{BASE_DIR}\\downloads")
    file.write("SQL Server Management Studio (SSMS) install successful\n")


if __name__ == "__main__":
    if(os.path.exists("C:\\Program Files (x86)\\Microsoft SQL Server Management Studio 18\\Common7\\IDE\\Ssms.exe")):
        file = open(rf"{BASE_DIR}\Logs\Result-Ssms-{get_current_date()}.txt", "w")
        file.write("Error")
        file.close()
        html = requests.get(URL_SITE, headers=headers)
        if html.status_code == 200:
            if(comparisons_version()):
                # Write log
                file = open(rf"{BASE_DIR}\Logs\Result-Ssms-{get_current_date()}.txt", "w")
                file.write("Successful\nNew version SQL Server Management Studio (SSMS) installed")
                file.close()
            else:
                # Install new version program
                get_download_and_install_file()
                
        else:
            # Write log
            file = open(rf"{BASE_DIR}\Logs\Result-Ssms-{get_current_date()}.txt", "w")
            file.write("Eror page\n")
            file.close()
    else:
        pass