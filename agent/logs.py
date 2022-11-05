import os

logs_archive = "/var/log/agent/logs"

def get_logs():
    return os.listdir(logs_archive)

def get_specific_log(log_name):
    if os.path.isfile(logs_archive+log_name):
        return(logs_archive+log_name)
    return "No such file: " + log_name