import os
import re

import logger

remote_logger = logger.get_remote_logger()
#offline_logger = logger.get_offline_logger()

def grep(filename, options):
    command = "grep {opt} {file}".format(opt=options, file=filename)
    remote_logger.debug("Created grep command: %s", command)
    try:
        remote_logger.info("Executing grep command: %s", command)
        os.system(command)
    except Exception as e:
        remote_logger.error("Error with grep command exectution %s", e)
        print("Wrong file or options" + e)
    
def parse_with_re(filename, options):
    result = []
    try:
        file = open(filename,'r')
        remote_logger.info("Succesfully opened file: %s, starting to analyze", filename)
        for line in file:
            if re.search(options, line):
                remote_logger.debug("Matched line: %s", line)
                result.append(line)
    except Exception as e:
        remote_logger.error("Error trying to open and parse a file %s", e)
        print(e)
    return result
