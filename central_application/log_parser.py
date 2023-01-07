import os
import re
import logger
import subprocess

def grep(filename, options):
    command = "grep {opt} {file}".format(opt=options, file=filename)
    output = ""
    try:
        output = subprocess.check_output(command, shell=True)
    except Exception as e:
        print("Wrong file or options" + e)
    return output.decode("utf-8") 
    
def parse_with_re(filename, options):
    result = []
    try:
        file = open(filename,'r')
        for line in file:
            if re.search(options, line):
                result.append(line)
    except Exception as e:
        print(e)
    return result
