import subprocess
from os.path import abspath, dirname
from datetime import date
import os

# Own Modules
import Zabbix.__zabbix_check as __zabbix_check
import GitHub_update.__git_hub_update as __git_hub_update
import Clean_logs.__clean_old_logs as __clean_old_logs

#########################


# Basik dir, where script execute
BASE_DIR = dirname(abspath(__file__))

# Repository where pull changes
URL_GIT_REPOSITORY = 'https://github.com/savyakvitalik/Update_program.git'

# DAYS after this will be delete old Logs
DAYS = 180

# Function for get current date	
def get_current_date():
    current_date = date.today()
    return current_date

# Function for run programs and writes errors in files
def run_program(file_name,main_list_error,list_error):
	if(os.path.exists("Logs")):
		pass
	else:
		os.mkdir("Logs")
	process = subprocess.Popen([f'{BASE_DIR}\\program_update\\{file_name}'],shell = True)
	process.wait()
	if process.returncode == 0:
		print("Success")
	else:
		main_list_error.append("Error")
		list_error.append(f"Error in {file_name}")
		print("Error")

if __name__ == "__main__":
	# Lists of errors
	main_list_error = [""]
	list_error = ["Errors: "]

	# Files which will be run
	file_names = [
			      '7zip_update.py',
				  'filezilla_update.py',
				  'notepad_update.py',
				  'totalcommander_update.py',
				  'Ssms_update.py'
			     ]
	# List of versions program
	list_versions = []

	#List paths to programs
	program_path = [
					'C:\\Program Files\\7-Zip\\7zG.exe',
					'C:\\Program Files\\Notepad++\\notepad++.exe',
					'C:\\Program Files\\FileZilla FTP Client\\filezilla.exe',
					'C:\\Program Files (x86)\\totalcmd\\TOTALCMD64.EXE',
					'C:\\Program Files\\totalcmd\\TOTALCMD64.EXE',
					'C:\\Program Files (x86)\\Microsoft SQL Server Management Studio 18\\Common7\\IDE\\Ssms.exe'
					]
	# Pull changes from repository
	__git_hub_update.git_pull(URL_GIT_REPOSITORY)

	# Cycle for run programs
	for name in file_names:
		run_program(name,main_list_error,list_error)

	# Cycle for check_version
	for path_name in program_path:
		__zabbix_check.get_program_version(path_name,list_versions)

	# Zabbix check
	__zabbix_check.zabbix_check(main_list_error,list_error)
	__zabbix_check.write_version_programs(list_versions)

	# Remove old logs
	__clean_old_logs.remove_old_logs(DAYS)