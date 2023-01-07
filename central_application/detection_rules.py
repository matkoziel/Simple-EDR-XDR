import re 
import pcap_analysis
import Evtx.Evtx as evtx
import xml.etree.ElementTree as ET
import Evtx.Views as e_views

def funkcja_testowa(**kwargs):
    error_counter = 0
    # Parse pcap
    if kwargs["pcap"] != '':
        print("Processing pcap")
        kwargs["pcap"]=pcap_analysis.traffic_from_file_pyshark(kwargs["pcap"],"")
        for pcap in kwargs["pcap"]:
            # only template
            pass

    # Parse evtx
    if kwargs["evtx"] != '':
        print("Processing evtx")
        result = ""
        with evtx.Evtx(kwargs["evtx"]) as event_log:
            result += e_views.XML_HEADER + "\n"
            result += "<Events>\n"
            for record in event_log.records():
                    result += record.xml() + "\n"
            result += "</Events>\n"

        for line in result:
            if re.search("error",txt,re.IGNORECASE):
                error_counter = error_counter + 1

    if kwargs["xml"] != '':
        print("Processing xml")
        for xml in kwargs["xml"]:
            # only template
            pass
    
    if kwargs["json"] != '':
        print("Processing json")
        for json in kwargs["json"]:
            # only template
            pass
    if kwargs["txt"] != '':
        with open(kwargs["txt"],"r") as txt_file:
            kwargs["txt"]=txt_file.readlines()
            txt_file.close()
        print("Processing txt")
        for txt in kwargs["txt"]:
            if re.search("error",txt,re.IGNORECASE):
                error_counter = error_counter + 1

    if error_counter > 2:
        action_alert = "remote" # remote local
        description = "Application may be down - More than 2 ERRORs occured"
    else:
        action_alert = None
        description = None
    return action_alert, description

def funkcja_testowa_2(**kwargs):
    print("Test 2")
    if True:
        action_alert = "local" # remote local
        description = "Local test"
    else:
        action_alert = None
        description = None
    return action_alert, description

def funkcja_testowa_3(**kwargs):
    print("Test 3")
    if True:
        action_alert = "local" # remote local
        description = "Local test"
    else:
        action_alert = None
        description = None
    return action_alert, description