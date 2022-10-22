import logging
import logging.handlers

#logging.basicConfig(filename="resources/log_parser.log",
#                    format='%(asctime)s %(levelname)s %(module)s.%(funcName)s %(message)s',
#                    filemode='w')

#logger = logging.getLogger()
#logger.setLevel(logging.DEBUG)

#def get_logger():
#    return logger

logger = logging.getLogger('Synchronous Logging')
http_handler = logging.handlers.HTTPHandler(
    '127.0.0.1:3000',
    '/insert_log',
    method='POST',
)
logger.addHandler(http_handler)

# Log messages:
logger.warning('Hey log a warning')
logger.error("Hey log a error")
