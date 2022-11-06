import ifcfg
import os
import pyshark
from pathlib import Path

pcaps_archive = os.environ.get('HOME') + "/.agent/pcaps/"

def get_network_config():
    return ifcfg.interfaces()

def sniff(interface, filter, file_name, sniff_time):
    Path(pcaps_archive).mkdir(parents=True, exist_ok=True)
    capture = pyshark.LiveCapture(interface=interface, bpf_filter=filter, output_file=(pcaps_archive + file_name))
    capture.sniff(timeout=sniff_time)
    return (pcaps_archive + file_name)

def get_pcaps():
    Path(pcaps_archive).mkdir(parents=True, exist_ok=True)
    return os.listdir(pcaps_archive)

def get_specific_pcap(pcap_name):
    if os.path.isfile(pcaps_archive+pcap_name):
        return(pcaps_archive+pcap_name)
    return -1

