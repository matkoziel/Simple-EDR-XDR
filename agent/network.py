import ifcfg
import json

def get_network_config():
    print(ifcfg.interfaces())
    return ifcfg.interfaces()


def sniffing():
    
