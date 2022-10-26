import logger
import pyshark

logger = logger.get_remote_logger()

def traffic_from_file_pyshark(path_to_file, filter):
    result = []
    try:
        logger.debug("Trying to open: {s}".format(s=path_to_file))
        traffic = pyshark.FileCapture(path_to_file, display_filter=filter)
        logger.debug("Filter applied: {s}".format(s=filter))
        for entry in traffic:
            result.append(entry)
    except Exception as exception:
        logger.error('Error while opening file: {s}'.format(s=path_to_file))
    return result

