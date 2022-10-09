import subprocess
from os.path import abspath, dirname
from datetime import date

# Basik dir, where script execute
BASE_DIR = dirname(abspath(__file__))

# Fuction for get current date
def get_current_date():
    current_date = date.today()
    return current_date

# Fuction for pull changes from repository on GitHub
def git_pull(Repository_url):
	process_git_reset = subprocess.Popen(['git','reset','--hard'],shell = True)
	process_git_reset.wait()
	process_git_pull = subprocess.Popen(['git','pull',f'{Repository_url}'],shell = True)
	process_git_pull.wait()
	file = open(rf"{BASE_DIR}\\last_update.txt", "w")
	file.write(f"Last update:\t {get_current_date()}")
	file.close()
	