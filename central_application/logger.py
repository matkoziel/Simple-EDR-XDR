import logging
import logging.handlers
from datetime import datetime
from jproperties import Properties

def log_action(function, output, time):
    filename = "Simple-EDR-XDR-" + function + "-" + time + ".log"
    with open(filename, "w") as file:
        file.write(output)
    

"""
offline_logger = logging.getLogger('Offline')

config = Properties()

logging.basicConfig(filename="resources/Simple-EDR-XDR-{time}.log".format(time=datetime.now().strftime("%d-%m-%Y-%H:%M:%S")),
#logging.basicConfig(filename="resources/Simple-EDR-XDR.log",
                   format='%(levelname)s %(asctime)s %(name)s %(module)s.%(funcName)s %(message)s',
                   filemode='w')

offline_logger.setLevel(logging.DEBUG)

def get_offline_logger():
   return offline_logger

with open('resources/app.properties','rb') as app_properties:
    config.load(app_properties,"utf-8")
host=config.get('REMOTE_LOGGER_HOST').data
port=config.get('REMOTE_LOGGER_PORT').data
uri=f"{host}:{port}"
remote_logger = logging.getLogger('Central Application')
http_handler = logging.handlers.HTTPHandler(
    uri,
    '/insert_log',
    method='POST',
)

remote_logger.addHandler(http_handler)

remote_logger.setLevel(logging.DEBUG)

def get_remote_logger():
    return remote_logger
"""


