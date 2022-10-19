import logging

logging.basicConfig(filename="resources/log_parser.log",
                    format='%(asctime)s %(levelname)s %(module)s.%(funcName)s %(message)s',
                    filemode='w')

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def get_logger():
    return logger