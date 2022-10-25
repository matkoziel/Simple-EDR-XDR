import logging
import logging.handlers


#logging.basicConfig(filename="resources\\\\log_parser.log",
#                    format='%(levelname)s %(asctime)s %(name)s %(module)s.%(funcName)s %(message)s',
#                    filemode='w')

#offline_logger = logging.getLogger()
# offline_logger.setLevel(logging.DEBUG)

#def get_offline_logger():
#    return offline_logger

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

