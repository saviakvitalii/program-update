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

#This url adress need change
URL_DOWNLOAD = 'https://download.filezilla-project.org/client/FileZilla__win64_sponsored2-setup.exe'
URL_SITE = 'https://download.filezilla-project.org/client/'

#Fuction for get current date
def get_current_date():
    current_date = date.today()
    return current_date

# Function for get old version program
def check_old_version():
    old_version_1 = subprocess.check_output(['powershell.exe',"(Get-Item \"C:\\Program Files\\FileZilla FTP Client\\filezilla.exe\").VersionInfo.FileVersion"], universal_newlines=True)
    old_version_2 = old_version_1.replace('.','').replace(' ','').replace(',','')
    old_version = old_version_2[:4]
    return old_version

#Fuction to check new version program
def check_new_version():
    httpx = requests.get(URL_SITE, headers=headers)
    html = httpx.text
    soup = BeautifulSoup(html, 'html.parser')
    urls = []
    for lines in soup.find_all("a"):
        urls.append(lines.get('href'))
    new_version = str(urls).split(",")[-7].replace('FileZilla_','').replace('_x86_64-linux-gnu.tar.bz2','')
    return new_version.replace("'","")


#Fuction to comparing old and new date
def comparisons_version():
    old_version = int(check_old_version())
    new_version_1 = check_new_version().replace('.','').replace(' ','').replace(',','').replace('-beta1','').replace('-rc1','')
    new_version = int(new_version_1)
    if (new_version - old_version) == 0:
        return True
    else:
        return False

def link_download():
    new_version = check_new_version()
    new_link = 'https://download.filezilla-project.org/client/FileZilla_'+ f"{new_version}" +'_win64_sponsored2-setup.exe'
    return new_link.replace(' ','')

# Function for get download file from website and install it
def get_download_and_install_file():
    file = open(rf"{BASE_DIR}\Logs\Result-filezilla-{get_current_date()}.txt", "w")
    if(os.path.exists("downloads")):
        shutil.rmtree("downloads")
    os.mkdir("downloads")
    Program_Name = f"{BASE_DIR}\\downloads\\filezilla.exe"
    file.write("Downloading...")
    with urllib.request.urlopen(link_download()) as response, open(Program_Name, 'wb') as out_file:
        shutil.copyfileobj(response, out_file)
    file.write("\tSUCCESS\n")
    file.write("Installing...")
    process = subprocess.Popen([f'{BASE_DIR}\\downloads\\filezilla.exe', '/S'])
    process.wait()
    file.write("\tSUCCESS\n")
    os.remove(f"{BASE_DIR}\\downloads\\filezilla.exe")
    shutil.rmtree("downloads")
    file.write("Filezilla updated successful\n")

if __name__ == "__main__":
    # Create and write personal log
    file = open(rf"{BASE_DIR}\Logs\Result-filezilla-{get_current_date()}.txt", "w")
    file.write("Error")
    file.close()
    if(os.path.exists("C:\\Program Files\\FileZilla FTP Client\\filezilla.exe")):
        html = requests.get(URL_SITE, headers=headers)
        # Check accessibility site
        if html.status_code == 200:
            if(comparisons_version()):
                # Write log
                file = open(rf"{BASE_DIR}\Logs\Result-filezilla-{get_current_date()}.txt", "w")
                file.write("Successful\nNew version 7-Zip installed")
                file.close()
            else:
                # Install new version program
                get_download_and_install_file()
        else:
            # Write log
            file = open(rf"{BASE_DIR}\Logs\Result-filezilla-{get_current_date()}.txt", "w")
            file.write("Eror page\n")
            file.close()
    else:
        html = requests.get(URL_SITE, headers=headers)
        # Check accessibility site
        if html.status_code == 200:
            # Install new version program
            get_download_and_install_file()
        else:
            # Write log
            file = open(rf"{BASE_DIR}\Logs\Result-filezilla-{get_current_date()}.txt", "w")
            file.write("Eror page\n")
            file.close()

    file.close()
    
