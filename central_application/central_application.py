import shutil
from pathlib import Path
import time
from beaupy import select_multiple
import click
import requests
import jsonify
from jproperties import Properties
import log_parser
import pcap_analysis
import os
#import logger
from logger import log_action
from inspect import getmembers, isfunction
from detection_rules import *

config = Properties()

def get_config():
    return config

def prepare_log(data):
    result=[]
    for log in data:
        one_log = "{time} {rule} {message}".format(time=log["timestamp"], rule=log["rule_name"],message=log["message"])
        result.append(one_log)
    return result


@click.group()
def cli():
    pass

@cli.group('parse_log')
def parse_log():
    pass

@parse_log.command('use_re')
@click.option('-r','--regex', type=click.STRING)
@click.option('-p','--path',type=click.File('r'),required=True)
def use_re(regex,path):
    act_time = (time.strftime('%d-%m-%Y-%H-%M-%S'))
    res = []
    if(regex):
        try:
            full_path = os.path.abspath(path.name)
            results = log_parser.parse_with_re(full_path,regex)
            for result in results:
                print(result,end='')
                res.append(result)
        except Exception as e:
            print(e)
            res.append(e)
    else:
        try:
            full_path = os.path.abspath(path.name)
            results = log_parser.parse_with_re(full_path,'')
            for result in results:
                print(result,end='')
                res.append(result)
        except Exception as e:
            print(e)
            res.append(e)
    log_action("use_re", res, act_time)

@parse_log.command('use_grep')
@click.option('-r','--regex',default='', type=click.STRING, required=True)
@click.option('-p','--path',type=click.File('r'),required=True)
def use_grep(regex,path):
    act_time = (time.strftime('%d-%m-%Y-%H-%M-%S'))
    res = []
    try:
        full_path = os.path.abspath(path.name)
        results = log_parser.grep(full_path,regex)
    except Exception as e:
        print(e)
    print(results)
    res.append(results)
    log_action("use_grep", res, act_time)

@cli.command('show_pcap')
@click.option('-p','--path',type=click.File('r'),required=True)
@click.option('-f','--filter',default='', type=click.STRING)
def show_pcap(path, filter):
    act_time = (time.strftime('%d-%m-%Y-%H-%M-%S'))
    res = []
    if filter:
        try:
            full_path = os.path.abspath(path.name)
            results = pcap_analysis.traffic_from_file_pyshark(full_path,filter)
            for r in results:
                print(r)
                res.append(r)
        except Exception as e:
            print(e)
            res.append(e)
    else:
        try:
            full_path = os.path.abspath(path.name)
            results = pcap_analysis.traffic_from_file_pyshark(full_path,"")
            for r in results:
                print(r)
                res.append(r)
        except Exception as e:
            print(e)
            res.append(e)
    log_action("show_pcap", res, act_time)

@cli.group('remote_logger')
def remote_logger():
    pass

@remote_logger.command('get_all_logs')
def get_all_logs():
    act_time = (time.strftime('%d-%m-%Y-%H-%M-%S'))
    res = []
    try:
        host=config.get('REMOTE_LOGGER_HOST').data
        port=config.get('REMOTE_LOGGER_PORT').data
        uri="http://{host}:{port}/get_logs".format(host=host,port=port)
        response = requests.get(url=uri)
        data = response.json()
        for i in prepare_log(data):
            print(i)
            res.append(i)
    except Exception as e:
        print(e)
        res.append(e)
    log_action("get_all_logs", res, act_time)

@remote_logger.command('get_logs')
@click.option('-r','--request',type=click.STRING)
def get_logs(request):
    act_time = (time.strftime('%d-%m-%Y-%H-%M-%S'))
    res = []
    try:
        host=config.get('REMOTE_LOGGER_HOST').data
        port=config.get('REMOTE_LOGGER_PORT').data
        uri="http://{host}:{port}/get_specific_logs".format(host=host,port=port)
        PARAMS = {'filter':request}
        response = requests.request(method='get', url=uri, json=PARAMS)
        data = response.json()
        for i in prepare_log(data):
            print(i)
            res.append(i)
    except Exception as e:
        print(e)
        res.append(e)
    log_action("get_logs", res, act_time)



@remote_logger.command('export_logs')
@click.option('-r','--request',type=click.STRING)
@click.option('-p','--path',type=click.File('w+'),required=True)
def get_logs(request, path):
    act_time = (time.strftime('%d-%m-%Y-%H-%M-%S'))
    res = []
    try:
        host=config.get('REMOTE_LOGGER_HOST').data
        port=config.get('REMOTE_LOGGER_PORT').data
        if request:
            uri="http://{host}:{port}/get_specific_logs".format(host=host,port=port)
            PARAMS = {'filter':request}
            response = requests.request(method='get', url=uri, json=PARAMS)
            data = response.json()
        else:
            uri="http://{host}:{port}/get_logs".format(host=host,port=port)
            PARAMS = {'filter':request}
            response = requests.request(method='get', url=uri, json=PARAMS)
            data = response.json()
        for i in prepare_log(data):
            path.write(i + '\n')
        path.close()
        res = [f"Data successfully written to file {path}"]
    except Exception as e:
        print(e)
    log_action("export_logs", res, act_time)

@cli.group('detection_rules')
def detection_rules():
    pass

@detection_rules.command("list_rules")
def list_rules():
    act_time = (time.strftime('%d-%m-%Y-%H-%M-%S'))
    res = []
    module = __import__("detection_rules")
    import detection_rules
    functions_list = getmembers(detection_rules, isfunction)
    for function_name in functions_list:
        print(function_name[0])
        res.append(function_name[0])
    log_action("list_rules", res, act_time)


@detection_rules.command("run_all_rules")
@click.option('-p','--pcap',type=click.STRING,default="")
@click.option('-e','--evtx',type=click.STRING,default="")
@click.option('-x','--xml',type=click.STRING,default="")
@click.option('-j','--json',type=click.STRING,default="")
@click.option('-t','--txt',type=click.STRING,default="")
def run_all_rules(pcap, evtx, xml, json, txt):
    act_time = (time.strftime('%d-%m-%Y-%H-%M-%S'))
    res = []
    host=config.get('REMOTE_LOGGER_HOST').data
    port=config.get('REMOTE_LOGGER_PORT').data
    module = __import__("detection_rules")
    import detection_rules
    functions_list_temp = getmembers(detection_rules, isfunction)
    functions_list = [i[0] for i in functions_list_temp]
    for function_name in functions_list:
        func = getattr(module, function_name)
        ret = func(pcap=pcap,evtx=evtx,xml=xml,json=json,txt=txt)
        if(ret[0] == 'remote'):
            uri = f"http://{host}:{port}/insert_log"
            PARAMS = {'rule_name':function_name,'msg':ret[1], 'timestamp':time.strftime('%d/%m/%Y %H:%M:%S')}
            response = requests.request(method='post', url=uri, json=PARAMS)
            print(f"Reguła {function_name} wywołała alert 'remote': {ret[1]}")
            res.append(f"Reguła {function_name} wywołała alert 'remote': {ret[1]}")
        elif (ret[0] == 'local'):
            print(f"Reguła {function_name} wywołała alert 'local': {ret[1]}")
            res.append(f"Reguła {function_name} wywołała alert 'local': {ret[1]}")
    log_action("run_rules", res, act_time)
        

@detection_rules.command("run_rules")
@click.option('-p','--pcap',type=click.STRING,default="")
@click.option('-e','--evtx',type=click.STRING,default="")
@click.option('-x','--xml',type=click.STRING,default="")
@click.option('-j','--json',type=click.STRING,default="")
@click.option('-t','--txt',type=click.STRING,default="")
def run_rules(pcap, evtx, xml, json, txt):
    act_time = (time.strftime('%d-%m-%Y-%H-%M-%S'))
    res = []
    host=config.get('REMOTE_LOGGER_HOST').data
    port=config.get('REMOTE_LOGGER_PORT').data
    module = __import__("detection_rules")
    import detection_rules
    functions_list_temp = getmembers(detection_rules, isfunction)
    functions_list = [i[0] for i in functions_list_temp]
    select = select_multiple(functions_list,minimal_count=1)
    for function_name in select:
        func = getattr(module, function_name)
        ret = func(pcap=pcap,evtx=evtx,xml=xml,json=json,txt=txt)
        if(ret[0] == 'remote'):
            uri = f"http://{host}:{port}/insert_log"
            PARAMS = {'rule_name':function_name,'msg':ret[1], 'timestamp':time.strftime('%d/%m/%Y %H:%M:%S')}
            response = requests.request(method='post', url=uri, json=PARAMS)
            print(f"Reguła {function_name} wywołała alert typu 'remote': {ret[1]}")
            res.append(f"Reguła {function_name} wywołała alert typu 'remote': {ret[1]}")
        elif (ret[0] == 'local'):
            print(f"Reguła {function_name} wywołała alert typu 'local': {ret[1]}")
            res.append(f"Reguła {function_name} wywołała alert typu 'local': {ret[1]}")
    log_action("run_rules", res, act_time)
        
        
@cli.group('remote_agent')
def remote_agent():
    pass

@remote_agent.command("cmd")
@click.option('-a','--agent',type=click.STRING, required=True)
@click.option('-p','--port',type=click.STRING, required=True)
@click.option('-c','--command',type=click.STRING)
def cmd(agent,port,command):
    act_time = (time.strftime('%d-%m-%Y-%H-%M-%S'))
    res = []
    uri=f"http://{agent}:{port}/execute_command"
    PARAMS = {'command':command}
    response = requests.request(method='post', url=uri, json=PARAMS)
    data = response.json()
    if (data is not None) or (data != ''):
        result = data['output'] 
        print (f'Result of {command} is: \n{result}')
        res.append(f'Result of {command} is: \n{result}')
    
    log_action("cmd", res, act_time)

@remote_agent.command("get_net_config")
@click.option('-a','--agent',type=click.STRING, required=True)
@click.option('-p','--port',type=click.STRING, required=True)
def get_net_config(agent,port):
    act_time = (time.strftime('%d-%m-%Y-%H-%M-%S'))
    res = []
    uri=f"http://{agent}:{port}/get_network_config"
    response = requests.get(url=uri)
    data = response.json()
    for line in data:
        print("Interface: " + line)
        res.append("Interface: " + line)
        for a in data[line]:
            print("\t" + str(a) + ": " + str(data[line][a]))
            res.append("\t" + str(a) + ": " + str(data[line][a]))
    log_action("get_net_config", res, act_time)

@remote_agent.command("capture_traffic")
@click.option('-a','--agent',type=click.STRING, required=True)
@click.option('-p','--port',type=click.STRING, required=True)
@click.option('-i','--interface',type=click.STRING, required=True)
@click.option('-f','--filter',type=click.STRING, default="")
@click.option('-w','--write',type=click.STRING, required=True)
@click.option('-t','--capture_time',type=click.STRING, required=True)
def capture_traffic(agent,port,interface,filter,write,capture_time):
    act_time = (time.strftime('%d-%m-%Y-%H-%M-%S'))
    res = []
    uri=f"http://{agent}:{port}/sniffing"
    PARAMS = {'interface':interface,'filter':filter,'file_name':write,'sniff_time':capture_time}
    response = requests.request(method='post', url=uri, json=PARAMS, headers={"Content-Type":"application/json"})
    with open(write, 'wb') as f:
        f.write(response.content)
        res.append(f"File {write} saved on local machine")
        print(f"File {write} saved on local machine")
    log_action("capture_traffic", res, act_time)

@remote_agent.command("get_logs_list")
@click.option('-a','--agent',type=click.STRING, required=True)
@click.option('-p','--port',type=click.STRING, required=True)
def list_logs(agent,port):
    act_time = (time.strftime('%d-%m-%Y-%H-%M-%S'))
    res = []
    uri=f"http://{agent}:{port}/get_log_list"
    response = requests.get(url=uri)
    data = response.json()
    print(f"Log files on agent {agent}:")
    res.append(f"Log files on agent {agent}:")
    for line in data:
        print(line)
        res.append(line)
    log_action("list_logs", res, act_time)

@remote_agent.command("get_chosen_log")
@click.option('-a','--agent',type=click.STRING, required=True)
@click.option('-p','--port',type=click.STRING, required=True)
@click.option('-f','--file',type=click.STRING, required=True)
def get_logs(agent,port,file):
    act_time = (time.strftime('%d-%m-%Y-%H-%M-%S'))
    res = []
    uri=f"http://{agent}:{port}/get_chosen_log"
    PARAMS = {'file':file}
    response = requests.request(method='get', url=uri, json=PARAMS, headers={"Content-Type":"application/json"})
    if not ("no such file" in str(response.content)):
        with open(file, 'wb') as f:
            f.write(response.content)
            res.append(f"File {file} saved on local machine")
            print(f"File {file} saved on local machine")
    else:
        print(f"File {file} not found on agent {agent}")
        res.append(f"File {file} not found on agent {agent}")
    log_action("get_logs", res, act_time)

@remote_agent.command("get_pcaps_list")
@click.option('-a','--agent',type=click.STRING, required=True)
@click.option('-p','--port',type=click.STRING, required=True)
def get_pcaps_list(agent,port):
    act_time = (time.strftime('%d-%m-%Y-%H-%M-%S'))
    res = []
    uri=f"http://{agent}:{port}/get_pcaps_list"
    response = requests.get(url=uri)
    data = response.json()
    print(f"PCAP files on agent {agent}:")
    res.append(f"PCAP files on agent {agent}:")
    for line in data:
        print(line)
        res.append(line)
    log_action("get_pcaps_list", res, act_time)

@remote_agent.command("get_chosen_pcap")
@click.option('-a','--agent',type=click.STRING, required=True)
@click.option('-p','--port',type=click.STRING, required=True)
@click.option('-f','--file',type=click.STRING, required=True)
def get_chosen_pcaps(agent,port,file):
    act_time = (time.strftime('%d-%m-%Y-%H-%M-%S'))
    res = []
    uri=f"http://{agent}:{port}/get_chosen_pcap"
    PARAMS = {'file':file}
    response = requests.request(method='get', url=uri, json=PARAMS, headers={"Content-Type":"application/json"})
    if not ("no such file" in str(response.content)):
        with open(file, 'wb') as f:
            f.write(response.content)
            res.append(f"File {file} saved on local machine")
            print(f"File {file} saved on local machine")
    else:
        print(f"File {file} not found on agent {agent}")
        res.append(f"File {file} not found on agent {agent}")
    log_action("get_logs", res, act_time)
    

@cli.group("SIGMA")
def SIGMA():
    pass

@SIGMA.command("add_new_ruleset")
@click.option('-f','--file',type=click.STRING,required=True)
def add_new_ruleset(file):
    act_time = (time.strftime('%d-%m-%Y-%H-%M-%S'))
    res = []
    path = Path(file)
    if path.is_file():
        #add file to SIGMA_rules
        shutil.copy2(path, "central_application/SIGMA_rules")
    if path.is_dir():
        #add files to SIGMA_rules
        files = os.listdir(path)
        for f in files:
            fp = Path(f)
            if fp.is_file():
                if fp.suffix in [".json",".evtx"]:
                    shutil.copy2(os.path.join(path,fp),"central_application/SIGMA_rules")
                else:
                    print(fp + " is not a valid file (use .json,.evtx)")
                    res.append(fp + " is not a valid file (use .json,.evtx)")
            else:
                print(fp, " is not a file")
                res.append(fp + " is not a file")
    else:
        print("bad file path")
        res.append("bad file path")
    print("New ruleset added")
    res.append("New ruleset added")
    log_action("add_new_ruleset", res, act_time)


@SIGMA.command("run_sigma")
@click.option('-e','--evtx',type=click.STRING,required=True)
@click.option('-r','--rules',type=click.STRING,default='',required=False)
def run_sigma(evtx,rules):
    act_time = (time.strftime('%d-%m-%Y-%H-%M-%S'))
    res = []
    print(f"Will run rules from: {rules} on logs in: {evtx}")
    res.append(f"Will run rules from: {rules} on logs in: {evtx}")
    #run zircolite
    cmd = "python central_application/Zircolite.py --evtx {}".format(evtx)
    if rules != '':
        cmd += (" --rules {}".format(rules))
    os.system(cmd)
    print("Check central_application/SIGMA_detected_events.json")
    res.append("Check central_application/SIGMA_detected_events.json")
    log_action("run_sigma", res, act_time)



if __name__ == '__main__':
    with open('resources/app.properties','rb') as app_properties:
        config.load(app_properties,"utf-8")
    cli()