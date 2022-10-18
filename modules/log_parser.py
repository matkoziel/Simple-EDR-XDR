import os
import re

def grep(filename, options):
    command = "grep {opt} {file}".format(opt=options, file=filename)
    try:
        os.system(command)
    except Exception as e:
        print("Wrong file or options" + e)
    
def parse_with_re(filename, options):
    result = []
    try:
        with open(filename,'r') as file:
            for line in file:
                if re.search(options, line):
                    result.append(line)
    except Exception as e:
        print(e)
    return result
