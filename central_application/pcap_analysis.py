import pyshark

def traffic_from_file_pyshark(path_to_file, filter):
    result = []
    try:
        traffic = pyshark.FileCapture(path_to_file, display_filter=filter)
        for entry in traffic:
            result.append(entry)
    except Exception as exception:
        print("Error: " + str(exception))
    return result

