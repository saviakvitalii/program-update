import os
from os.path import abspath, dirname
from datetime import date


# Basik dir, where script execute
BASE_DIR = dirname(dirname(abspath(__file__)))


# Function for get current date
def get_current_date():
    current_date = date.today()
    return str(current_date).replace('-','')

# Function for remove old logs
def remove_old_logs(days):
    if(os.path.exists("{BASE_DIR}\\Logs")):
        # Dir, where takes file log
        dir_list = os.listdir(f"{BASE_DIR}\\Logs")
        for file in dir_list:
            if (int(get_current_date()) - int(file[-14:].replace('-','').replace('.txt','')) > days):
                os.remove(f"{BASE_DIR}\\Logs\\{file}")
            else:
                pass
    else:
        pass

