import re 
import pcap_analysis
import Evtx.Evtx as evtx 
import xml.etree.ElementTree as ET

def funkcja_testowa(**kwargs):

    kwargs["pcap"]=pcap_analysis.traffic_from_file_pyshark(kwargs["pcap"],"")
    for pcap in kwargs["pcap"]:
        pass

    with evtx.Evtx(kwargs["evtx"]) as event_log:
        # res=[]
        # for record in event_log.records():
        #     res.append(record.lxml())
        # kwargs["evtx"]=res

        root = ET.fromstring(event_log.records())
    print(root.findall("0x8000000000000000"))
    # for evtx_ in kwargs["evtx"]:
        

    for xml in kwargs["xml"]:
        # procesowanie json
        pass

    for json in kwargs["json"]:
        # procesowanie txt
        pass
    
    with open(kwargs["txt"],"r") as txt_file:
        kwargs["txt"]=txt_file.readlines()
        txt_file.close()
    for txt in kwargs["txt"]:
        if re.search("error",txt,re.IGNORECASE):
            print("ERROR")

    if True==True:
        action_alert = "..." # akcja: "local", "remote"
        description = "Alert ..."
    else:
        action_alert = None
        description = None
    return action_alert, description

def funkcja_2(**kwargs):
    print("123xD")