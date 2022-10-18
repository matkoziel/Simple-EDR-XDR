import libpcap

def traffic_from_file_libpcap(path_to_file, filter):
    try:
        traffic = libpcap.open_offline(offline = path_to_file, filter = filter)
        for entry in traffic:
            print(entry)
    except Exception as exception:
        print('Invalid path to file')

import pyshark

def traffic_from_file_pyshark(path_to_file, filter):
    try:   
        traffic = pyshark.FileCapture(path_to_file, display_filter=filter)
        for entry in traffic:
            print(entry)
    except Exception as exception:
        print('Invalid path to file')