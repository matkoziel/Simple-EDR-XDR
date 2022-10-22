import logger
import libpcap

logger = logger.get_remote_logger()

def traffic_from_file_libpcap(path_to_file, filter):
    try:
        logger.debug("Trying to open: %s", path_to_file)
        traffic = libpcap.open_offline(offline = path_to_file, filter = filter)
        logger.debug("Filter applied: %s", filter)
        for entry in traffic:
            print(entry)
    except Exception as exception:
        logger.error('Error while opening file: %s', path_to_file)

import pyshark

def traffic_from_file_pyshark(path_to_file, filter):
    try:
        logger.debug("Trying to open: %s", path_to_file)
        traffic = pyshark.FileCapture(path_to_file, display_filter=filter)
        logger.debug("Filter applied: %s", filter)
        for entry in traffic:
            print(entry)
    except Exception as exception:
        logger.error('Error while opening file: %s', path_to_file)