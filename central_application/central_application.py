from beaupy import select_multiple
import click
import requests
from jproperties import Properties
import log_parser
import pcap_analysis
import os
import logger
from inspect import getmembers, isfunction
from detection_rules import *

config = Properties()

def get_config():
    return config

def prepare_log(data):
    result=[]
    for log in data:
        one_log = "{date} {time} {type} {app} {module} {message}".format(date=log["date"], time=log["time"], type=log["type"], app=log["logger"], module=log["module"], message=log["message"])
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
    if(regex):
        try:
            full_path = os.path.abspath(path.name)
            results = log_parser.parse_with_re(full_path,regex)
            for result in results:
                print(result,end='')
        except Exception as e:
            print(e)
    else:
        try:
            full_path = os.path.abspath(path.name)
            results = log_parser.parse_with_re(full_path,'')
            for result in results:
                print(result,end='')
        except Exception as e:
            print(e)

@parse_log.command('use_grep')
@click.option('-r','--regex',default='', type=click.STRING, required=True)
@click.option('-p','--path',type=click.File('r'),required=True)
def use_grep(regex,path):
    try:
        full_path = os.path.abspath(path.name)
        log_parser.grep(full_path,regex)
    except Exception as e:
        print(e)

@cli.command('show_pcap')
@click.option('-p','--path',type=click.File('r'),required=True)
@click.option('-f','--filter',default='', type=click.STRING)
def show_pcap(path, filter):
    if filter:
        try:
            full_path = os.path.abspath(path.name)
            result = pcap_analysis.traffic_from_file_pyshark(full_path,filter)
            for res in result:
                print(res)
        except Exception as e:
            print(e)
    else:
        try:
            full_path = os.path.abspath(path.name)
            result = pcap_analysis.traffic_from_file_pyshark(full_path,"")
            for res in result:
                print(res)
        except Exception as e:
            print(e)

@cli.group('remote_logger')
def remote_logger():
    pass

@remote_logger.command('get_all_logs')
def get_all_logs():
    try:
        host=config.get('REMOTE_LOGGER_HOST').data
        port=config.get('REMOTE_LOGGER_PORT').data
        uri="http://{host}:{port}/get_logs".format(host=host,port=port)
        resposne = requests.get(url=uri)
        data = resposne.json()
        for i in prepare_log(data):
            print(i)
    except Exception as e:
        print(e)

@remote_logger.command('get_logs')
@click.option('-r','--request',type=click.STRING)
def get_logs(request):
    try:
        host=config.get('REMOTE_LOGGER_HOST').data
        port=config.get('REMOTE_LOGGER_PORT').data
        uri="http://{host}:{port}/get_specific_logs".format(host=host,port=port)
        PARAMS = {'filter':request}
        resposne = requests.request(method='get', url=uri, data=PARAMS)
        data = resposne.json()
        for i in prepare_log(data):
            print(i)
    except Exception as e:
        print(e)

@remote_logger.command('export_logs')
@click.option('-r','--request',type=click.STRING)
@click.option('-p','--path',type=click.File('w+'),required=True)
def get_logs(request, path):
    try:
        host=config.get('REMOTE_LOGGER_HOST').data
        port=config.get('REMOTE_LOGGER_PORT').data
        if request:
            uri="http://{host}:{port}/get_specific_logs".format(host=host,port=port)
            PARAMS = {'filter':request}
            resposne = requests.request(method='get', url=uri, data=PARAMS)
            data = resposne.json()
        else:
            uri="http://{host}:{port}/get_logs".format(host=host,port=port)
            PARAMS = {'filter':request}
            resposne = requests.request(method='get', url=uri, data=PARAMS)
            data = resposne.json()
        for i in prepare_log(data):
            path.write(i + '\n')
        path.close()
    except Exception as e:
        print(e)

@cli.group('detection_rules')
def detection_rules():
    pass

@detection_rules.command("list_rules")
def list_rules():
    module = __import__("detection_rules")
    import detection_rules
    functions_list = getmembers(detection_rules, isfunction)
    for function_name in functions_list:
        print(function_name)

@detection_rules.command("run_all_rules")
@click.option('-p','--pcap',type=click.STRING,default="")
@click.option('-e','--evtx',type=click.STRING,default="")
@click.option('-x','--xml',type=click.STRING,default="")
@click.option('-j','--json',type=click.STRING,default="")
@click.option('-t','--txt',type=click.STRING,default="")
def run_all_rules(pcap, evtx, xml, json, txt):
    module = __import__("detection_rules")
    import detection_rules
    functions_list = getmembers(detection_rules, isfunction)
    for function_name in functions_list:
        func = getattr(module, function_name[0])
        func(pcap=pcap,evtx=evtx,xml=xml,json=json,txt=txt)

@detection_rules.command("run_rules")
@click.option('-p','--pcap',type=click.STRING,default="")
@click.option('-e','--evtx',type=click.STRING,default="")
@click.option('-x','--xml',type=click.STRING,default="")
@click.option('-j','--json',type=click.STRING,default="")
@click.option('-t','--txt',type=click.STRING,default="")
def run_rules(pcap, evtx, xml, json, txt):
    module = __import__("detection_rules")
    import detection_rules
    functions_list_temp = getmembers(detection_rules, isfunction)
    functions_list = [i[0] for i in functions_list_temp]
    select = select_multiple(functions_list,minimal_count=1)
    for function_name in select:
        func = getattr(module, function_name)
        func(pcap=pcap,evtx=evtx,xml=xml,json=json,txt=txt)

@cli.group('remote_agent')
def remote_agent():
    pass

@remote_agent.command("get_net_config")
@click.option('-a','--agent',type=click.STRING, required=True)
@click.option('-p','--port',type=click.STRING, required=True)
def get_net_config(agent,port):
    uri=f"http://{agent}:{port}/get_network_config"
    resposne = requests.get(url=uri)
    data = resposne.json()
    print(data)

@remote_agent.command("capture_traffic")
@click.option('-a','--agent',type=click.STRING, required=True)
@click.option('-p','--port',type=click.STRING, required=True)
@click.option('-i','--interface',type=click.STRING, required=True)
@click.option('-f','--filter',type=click.STRING, default="")
@click.option('-w','--write',type=click.STRING, required=True)
@click.option('-t','--time',type=click.STRING, required=True)
def capture_traffic(agent,port,interface,filter,write,time):
    uri=f"http://{agent}:{port}/sniffing"
    PARAMS = {'interface':interface,'filter':filter,'file_name':write,'sniff_time':time}
    resposne = requests.request(method='post', url=uri, json=PARAMS, headers={"Content-Type":"application/json"})
    data = resposne.json()
    print(data)

@remote_agent.command("list_logs")
@click.option('-a','--agent',type=click.STRING, required=True)
@click.option('-p','--port',type=click.STRING, required=True)
def list_logs(agent,port):
    uri=f"http://{agent}:{port}/get_log_list"
    resposne = requests.get(url=uri)
    data = resposne.json()
    print(f"Log files on agent {agent}:{port}:")
    print(data)

@remote_agent.command("get_logs")
@click.option('-a','--agent',type=click.STRING, required=True)
@click.option('-p','--port',type=click.STRING, required=True)
@click.option('-f','--file',type=click.STRING, required=True)
def get_logs(agent,port,file):
    uri=f"http://{agent}:{port}/get_chosen_logs"
    resposne = requests.get(url=uri)
    PARAMS = {'file':file}
    resposne = requests.request(method='get', url=uri, json=PARAMS, headers={"Content-Type":"application/json"})
    data = resposne.json()
    print(f"Log files on agent {agent}:{port}:")
    print(data)

@remote_agent.command("get_pcaps_list")
@click.option('-a','--agent',type=click.STRING, required=True)
@click.option('-p','--port',type=click.STRING, required=True)
def get_pcaps_list(agent,port):
    uri=f"http://{agent}:{port}/get_pcaps_list"
    resposne = requests.get(url=uri)
    data = resposne.json()
    print(f"Log files on agent {agent}:{port}:")
    print(data)

@remote_agent.command("get_chosen_pcaps")
@click.option('-a','--agent',type=click.STRING, required=True)
@click.option('-p','--port',type=click.STRING, required=True)
@click.option('-f','--file',type=click.STRING, required=True)
def get_chosen_pcaps(agent,port,file):
    uri=f"http://{agent}:{port}/get_chosen_pcaps"
    resposne = requests.get(url=uri)
    PARAMS = {'file':file}
    resposne = requests.request(method='get', url=uri, json=PARAMS, headers={"Content-Type":"application/json"})
    data = resposne.json()
    print(f"Log files on agent {agent}:{port}:")
    print(data)
    

@remote_agent.command("cmd")
@click.option('-a','--agent',type=click.STRING, required=True)
@click.option('-p','--port',type=click.STRING, required=True)
@click.option('-c','--command',type=click.STRING)
def cmd(agent,port,command):
    uri=f"http://{agent}:{port}/execute_command"
    PARAMS = {'command':command}
    resposne = requests.request(method='post', url=uri, json=PARAMS)
    data = resposne.json()
    if (data is not None) or (data != ''):
        result = data['output'] 
        print (f'Result of {command} is: \n{result}')


if __name__ == '__main__':
    with open('resources/app.properties','rb') as app_properties:
        config.load(app_properties,"utf-8")
    offline_logger=logger.get_offline_logger()
    cli()