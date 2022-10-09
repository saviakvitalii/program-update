import requests
from datetime import date
from os.path import abspath, dirname, join
from bs4 import BeautifulSoup
import urllib.request
import os
import shutil
import subprocess
import ssl
###########################

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    # Legacy Python that doesn't verify HTTPS certificates by default
    pass
else:
    # Handle target environment that doesn't support HTTPS verification
    ssl._create_default_https_context = _create_unverified_https_context

###########################
# Basik dir, where script execute
BASE_DIR = dirname(dirname(abspath(__file__)))

# URL main website
URL = 'https://www.7-zip.org/download.html'

# Function for get current date
def get_current_date():
    current_date = date.today()
    return current_date

# Function for get old version program
def check_old_version():
    old_version = subprocess.check_output(['powershell.exe',"(Get-Item \"C:\\Program Files\\7-Zip\\7zG.exe\").VersionInfo.FileVersion"], universal_newlines=True)
    return old_version.replace('.','').replace(' ','').replace(',','')

# Function for get url page
def get_html(url):
    r = requests.get(url)
    return r

# Function for get url text
def get_html_text(url):
    r = requests.get(url)
    return r.text

# Function for get new version program on website
def check_new_version(html):
    soup = BeautifulSoup(html, 'html.parser')
    page_text = soup.find_all("b")
    txt = page_text[1].getText()
    new_version = txt[15:20]
    return new_version.replace('.','').replace(' ','').replace(',','')

# Function for compare new and old version
def comparisons_version():
    new_version = float(check_new_version(get_html_text(URL)))
    old_version = float(check_old_version())
    if (new_version - old_version) == 0:
        return True
    else:
        return False
        
# Function for get download link
def get_download_link(html):
    soup = BeautifulSoup(html, 'html.parser')
    urls = []
    for link in soup.find_all('a'): 
        urls.append(link.get('href'))
    download_link = "https://www.7-zip.org/" + urls[18]
    return download_link

# Function for get download file from website and install it
def get_download_and_install_file(result_url):
    file = open(rf"{BASE_DIR}\Logs\Result-7zip-{get_current_date()}.txt", "w")
    if(os.path.exists("downloads")):
        shutil.rmtree("downloads")
    os.mkdir("downloads")
    Program_Name = f"{BASE_DIR}\\downloads\\7zip.exe"
    file.write("Downloading...")
    with urllib.request.urlopen(result_url) as response, open(Program_Name, 'wb') as out_file:
        shutil.copyfileobj(response, out_file)
    file.write("\tSUCCESS\n")
    file.write("Installing...")
    process = subprocess.Popen([f'{BASE_DIR}\\downloads\\7zip.exe', '/S'])
    process.wait()
    file.write("\tSUCCESS\n")
    os.remove(f"{BASE_DIR}\\downloads\\7zip.exe")
    shutil.rmtree("downloads")
    file.write("7-Zip updated successful\n")
    file.close()

if __name__ == "__main__":
    # Create and write personal log
    file = open(rf"{BASE_DIR}\Logs\Result-7zip-{get_current_date()}.txt", "w")
    file.write("Error")
    file.close()
    if(os.path.exists("C:\\Program Files\\7-Zip\\7zG.exe")):
        html = get_html(URL)
        # Check accessibility site
        if html.status_code == 200:
            if(comparisons_version()):
                # Write log
                file = open(rf"{BASE_DIR}\Logs\Result-7zip-{get_current_date()}.txt", "w")
                file.write("Successful\nNew version 7-Zip installed")
                file.close()
            else:
                # Install new version program
                result_url = get_download_link(get_html_text(URL))
                get_download_and_install_file(result_url)
        else:
            # Write log
            file = open(rf"{BASE_DIR}\Logs\Result-7zip-{get_current_date()}.txt", "w")
            file.write("Eror page\n")
            file.close()
    else:
        html = get_html(URL)
        # Check accessibility site
        if html.status_code == 200:
            # Install new version program
            result_url = get_download_link(get_html_text(URL))
            get_download_and_install_file(result_url)
        else:
            # Write log
            file = open(rf"{BASE_DIR}\Logs\Result-7zip-{get_current_date()}.txt", "w")
            file.write("Eror page\n")
            file.close()

    file.close()