import re 
import pcap_analysis
import Evtx.Evtx as evtx 
import xml.etree.ElementTree as ET
import Evtx.Views as e_views

def funkcja_testowa(**kwargs):

    # Parse pcap
    kwargs["pcap"]=pcap_analysis.traffic_from_file_pyshark(kwargs["pcap"],"")
    for pcap in kwargs["pcap"]:
        pass

    # Parse evtx
    with evtx.Evtx(kwargs["evtx"]) as event_log:
       result = ""
       result += e_views.XML_HEADER + "\n"
       result += "<Events>\n"
       for record in event_log.records():
            result+=record.xml() + "\n"
       result += "</Events>\n"

    print(result)

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