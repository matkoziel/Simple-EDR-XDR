import os
from pathlib import Path

logs_archive = os.environ.get('HOME') + "/.agent/logs/"

def get_logs():
    Path(logs_archive).mkdir(parents=True, exist_ok=True)
    return os.listdir(logs_archive)

def get_specific_log(log_name):
    if os.path.isfile(logs_archive+log_name):
        print(logs_archive+log_name)
        return(logs_archive+log_name)
    return -1