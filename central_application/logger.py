import logging
import logging.handlers
from datetime import datetime


offline_logger = logging.getLogger('Offline')

logging.basicConfig(filename="resources/Simple-EDR-XDR-{time}.log".format(time=datetime.now().strftime("%d-%m-%Y-%H:%M:%S")),
                   format='%(levelname)s %(asctime)s %(name)s %(module)s.%(funcName)s %(message)s',
                   filemode='w')

offline_logger.setLevel(logging.DEBUG)

def get_offline_logger():
   return offline_logger

remote_logger = logging.getLogger('Central Application')
http_handler = logging.handlers.HTTPHandler(
    '127.0.0.1:3000',
    '/insert_log',
    method='POST',
)

remote_logger.addHandler(http_handler)

remote_logger.setLevel(logging.DEBUG)

def get_remote_logger():
    return remote_logger
