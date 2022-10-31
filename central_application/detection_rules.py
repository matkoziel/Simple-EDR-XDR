
def funkcja_testowa(**kwargs):
    print(kwargs)
# ciało funkcji - właściwa reguła operująca na danych z args
# procesowanie pcap
    for pcap in kwargs["pcap"]:
        print(pcap)
        pass
    for evtx in kwargs["evtx"]:
        # procesowanie xml
        pass
    for xml in kwargs["xml"]:
        # procesowanie json
        pass
    for json in kwargs["json"]:
        # procesowanie txt
        pass
    for txt in kwargs["txt"]:
        pass

    if True==True:
        action_alert = "..." # akcja: "local", "remote"
        description = "Alert ..."
    else:
        action_alert = None
        description = None
    return action_alert, description

def funkcja_2(**kwargs):
    print("123xD")