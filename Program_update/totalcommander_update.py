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

headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '\
           'AppleWebKit/537.36 (KHTML, like Gecko) '\
           'Chrome/75.0.3770.80 Safari/537.36'}

###########################
# Basik dir, where script execute
BASE_DIR = dirname(dirname(abspath(__file__)))

# URL main website
URL = 'https://www.ghisler.com/download.htm'

# Function for get current date
def get_current_date():
    current_date = date.today()
    return current_date

# Function for get url page
def get_html(url):
    r = requests.get(url, headers=headers)
    return r

# Function for get url text
def get_html_text(url):
    r = requests.get(url, headers=headers)
    return r.text

# Functions for get old version program
def check_old_version_32bit_1():
    old_version = subprocess.check_output(['powershell.exe',"(Get-Item \"C:\\Program Files\\totalcmd\\TOTALCMD.EXE\").VersionInfo.FileVersion"], universal_newlines=True)
    return old_version
def check_old_version_64bit_1():
    old_version = subprocess.check_output(['powershell.exe',"(Get-Item \"C:\\Program Files\\totalcmd\\TOTALCMD64.EXE\").VersionInfo.FileVersion"], universal_newlines=True)
    return old_version
def check_old_version_32bit_2():
    old_version = subprocess.check_output(['powershell.exe',"(Get-Item \"C:\\Program Files (x86)\\totalcmd\\TOTALCMD.EXE\").VersionInfo.FileVersion"], universal_newlines=True)
    return old_version
def check_old_version_64bit_2():
    old_version = subprocess.check_output(['powershell.exe',"(Get-Item \"C:\\Program Files (x86)\\totalcmd\\TOTALCMD64.EXE\").VersionInfo.FileVersion"], universal_newlines=True)
    return old_version

# Function for check old version program
def check_old_version():
    if(os.path.exists("C:\\Program Files\\totalcmd\\TOTALCMD.EXE")):
        old_version_1 = check_old_version_32bit_1()
    elif(os.path.exists("C:\\Program Files\\totalcmd\\TOTALCMD64.EXE")):
        old_version_1 = check_old_version_64bit_1()
    elif(os.path.exists("C:\\Program Files (x86)\\totalcmd\\TOTALCMD.EXE")):
        old_version_1 = check_old_version_32bit_2()
    elif(os.path.exists("C:\\Program Files (x86)\\totalcmd\\TOTALCMD64.EXE")):
        old_version_1 =check_old_version_64bit_2()

    return old_version_1.replace('.','').replace(' ','').replace(',','')[:4]

# Function for get new version program on website
def check_new_version(html):
    soup = BeautifulSoup(html, 'html.parser')
    txt = soup.find("h3")
    txt1 = txt.text
    full_version = txt1.split(' ')
    version = full_version[9]
    return version.replace('.','').replace(' ','').replace(',','')

# Function for compare new and old version
def comparisons_version():
    old_version = int(check_old_version())
    new_version = int(check_new_version(get_html_text(URL)))
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
    return urls[16]

# Function for get download file from website and install it
def get_download_and_install_file(result_url):
    file = open(rf"{BASE_DIR}\Logs\Result-totalCommander-{get_current_date()}.txt", "w")
    if(os.path.exists("downloads")):
        shutil.rmtree("downloads")
    os.mkdir("downloads")
    Program_Name = f"{BASE_DIR}\\downloads\\TotalCommander.exe"
    file.write("Downloading...")
    with urllib.request.urlopen(result_url) as response, open(Program_Name, 'wb') as out_file:
        shutil.copyfileobj(response, out_file)
    file.write("\tSUCCESS\n")
    file.write("Installing...")
    process = subprocess.Popen([f'{BASE_DIR}\\downloads\\TotalCommander.exe', '/AHMGDU'])
    process.wait()
    file.write("\tSUCCESS\n")
    os.remove(f"{BASE_DIR}\\downloads\\TotalCommander.exe")
    shutil.rmtree("downloads")
    file.write("TotalCommander updated successful\n")

if __name__ == "__main__":
    # Create and write personal log
    file = open(rf"{BASE_DIR}\Logs\Result-totalCommander-{get_current_date()}.txt", "w")
    file.write("Error")
    file.close()
    #Check of exist totalcommander
    if(os.path.exists("C:\\Program Files\\totalcmd\\TOTALCMD.EXE")) or (os.path.exists("C:\\Program Files\\totalcmd\\TOTALCMD64.EXE")):
        html = get_html(URL)
        # Check accessibility site
        if html.status_code == 200:
            if(comparisons_version()):
                # Write log
                file = open(rf"{BASE_DIR}\Logs\Result-totalCommander-{get_current_date()}.txt", "w")
                file.write("Successful\nNew version TotalCommander installed")
            else:
                # Install new version program
                result_url = get_download_link(get_html_text(URL))
                get_download_and_install_file(result_url)
        else:
            # Write log
            file = open(rf"{BASE_DIR}\Logs\Result-totalCommander-{get_current_date()}.txt", "w")
            file.write("Eror page\n")
    #Check of exist totalcommander
    elif (os.path.exists("C:\\Program Files (x86)\\totalcmd\\TOTALCMD64.EXE")) or (os.path.exists("C:\\Program Files (x86)\\totalcmd\\TOTALCMD.EXE")):
        html = get_html(URL)
        # Check accessibility site
        if html.status_code == 200:
            if(comparisons_version()):
                # Write log
                file = open(rf"{BASE_DIR}\Logs\Result-totalCommander-{get_current_date()}.txt", "w")
                file.write("Successful\nNew version TotalCommander installed")
            else:
                # Install new version program
                result_url = get_download_link(get_html_text(URL))
                get_download_and_install_file(result_url)
        else:
            # Write log
            file = open(rf"{BASE_DIR}\Logs\Result-totalCommander-{get_current_date()}.txt", "w")
            file.write("Eror page\n")

    else:
        html = get_html(URL)
        # Check accessibility site
        if html.status_code == 200:
            # Install new version program
            result_url = get_download_link(get_html_text(URL))
            get_download_and_install_file(result_url)
        else:
            # Write log
            file = open(rf"{BASE_DIR}\Logs\Result-totalCommander-{get_current_date()}.txt", "w")
            file.write("Eror page\n")

    file.close()

