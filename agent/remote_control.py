import subprocess

def execute_command(command):
    output = subprocess.getoutput(command)
    return output
