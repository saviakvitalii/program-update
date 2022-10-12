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
url_text = 'https://notepad-plus-plus.org/'

# Function for get current date
def get_current_date():
    current_date = date.today()
    return current_date

# Function for get old version program
def check_old_version():
    old_version = subprocess.check_output(['powershell.exe',"(Get-Item \"C:\\Program Files\\Notepad++\\notepad++.exe\").VersionInfo.FileVersion"], universal_newlines=True)
    return old_version.replace('.','').replace(' ','').replace(',','')

# Function for get url page
def get_html(url, params=None):
    r = requests.get(url, headers=headers)
    return r

#Function of getting url page
def get_download_page(html):
    soup = BeautifulSoup(html, 'html.parser')
    urls = []
    for link in soup.find_all('a'): 
        urls.append(link.get('href'))
    url_download = urls[2]
    download_page = url_text + url_download
    return download_page


# Function for get new version program on website
def check_new_version(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find('p', class_='library-desc')
    txt = items.text
    new_version = txt[17:]       
    return new_version.replace('.','').replace(' ','').replace(',','')


#Function of getting url download
def get_url_download(html):
    soup = BeautifulSoup(html, 'html.parser')
    urls = []
    for link in soup.find_all('a'):
        urls.append(link.get('href')) 
    url_download = urls[12]
    return url_download


# Function for compare new and old version
def comparisons_version():
    html_1 = get_html(url_text)
    old_version = int(check_old_version())
    new_version = int(check_new_version(html_1.text))
    if (new_version - old_version) == 0:
        return True
    else:
        return False


# Function for get download file from website and install it
def get_download_and_install_file(result_url):
    file = open(rf"{BASE_DIR}\Logs\Result-notepad-{get_current_date()}.txt", "w")
    if(os.path.exists("downloads")):
        shutil.rmtree("downloads")
    os.mkdir("downloads")
    Program_Name = f"{BASE_DIR}\\downloads\\notepad++.exe"
    file.write("Downloading...")
    with urllib.request.urlopen(result_url) as response, open(Program_Name, 'wb') as out_file:
        shutil.copyfileobj(response, out_file)
    file.write("\tSUCCESS\n")
    file.write("Installing...")
    process = subprocess.Popen([f'{BASE_DIR}\\downloads\\notepad++.exe', '/S'])
    process.wait()
    file.write("\tSUCCESS\n")
    os.remove(f"{BASE_DIR}\\downloads\\notepad++.exe")
    shutil.rmtree("downloads")
    file.write("Notepad++ install successful\n")

if __name__ == "__main__":
    # Create and write personal log
    file = open(rf"{BASE_DIR}\Logs\Result-notepad-{get_current_date()}.txt", "w")
    file.write("Error")
    file.close()
    #Check of exist notepad++
    if(os.path.exists("C:\\Program Files\\Notepad++\\notepad++.exe")):
        html_1 = get_html(url_text)
        # Check accessibility site   
        if(html_1.status_code) == 200:
            if(comparisons_version()):
                # Write log
                file = open(rf"{BASE_DIR}\Logs\Result-notepad-{get_current_date()}.txt", "w")
                file.write("Successful\nNew version notepad++ installed")
            else:
                # Get download page
                url_page = get_download_page(html_1.text)
                html_2 = get_html(url_page)
                # Check accessibility site
                if(html_2.status_code) == 200:
                    # Install new version program
                    result_url = get_url_download(html_2.text)
                    get_download_and_install_file(result_url)
                else:
                    # Write log
                    file = open(rf"{BASE_DIR}\Logs\Result-notepad-{get_current_date()}.txt", "w")
                    file.write("Eror second page\n")
        else:
            # Write log
            file = open(rf"{BASE_DIR}\Logs\Result-notepad-{get_current_date()}.txt", "w")
            file.write("Eror first page\n")
    else:
        # Check accessibility site
        html_3 = get_html(url_text)  
        if(html_3.status_code) == 200:
            # Get download page
            url_page = get_download_page(html_3.text)
            html_4 = get_html(url_page)
            # Check accessibility site
            if(html_4.status_code) == 200:
                # Install new version program
                result_url = get_url_download(html_4.text)
                get_download_and_install_file(result_url)
            else:
                # Write log
                file = open(rf"{BASE_DIR}\Logs\Result-notepad-{get_current_date()}.txt", "w")
                file.write("Eror second page\n")
        else:
            # Write log
            file.write("Eror first page\n")

    file.close()

