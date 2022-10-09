import subprocess
from os.path import abspath, dirname
import os

# Basik dir, where script execute
BASE_DIR = dirname(abspath(__file__))
ZABBIX_DIR = 'C:\Program Files\ZabbixAgent\log'
# Function for check error
def zabbix_check(main_list_error,list_error):
	for word in main_list_error:
		if word == "Error":
			file = open(rf"{ZABBIX_DIR}\program_update.txt", "w")
			file.write(f"{list_error}")
			file.close()
		else:
			file = open(rf"{ZABBIX_DIR}\program_update.txt", "w")
			file.write("True")
			file.close()

#Fuction for det program version
def get_program_version(program_path, list_versions):
	if(os.path.exists(f"{program_path}")):
		version = subprocess.check_output(['powershell.exe',f"(Get-Item \"{program_path}\").VersionInfo.ProductVersion"], universal_newlines=True)
		list_versions.append(f"{program_path} --- {version}\n")
	else:
		pass
	
#Fuction for write programs version in file
def write_version_programs(list_versions):
    new_string = ""
    for name in list_versions:
        new_string += name
    file = open(f"{ZABBIX_DIR}\program_version.txt", "w")
    file.write(f"{new_string}")
    file.close()