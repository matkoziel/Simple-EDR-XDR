from email import message
import click
import requests
from jproperties import Properties
import log_parser
import pcap_analysis
import os

def prepare_log(data):
    result=[]
    for log in data:
        one_log = "{date} \t{time}\t{type}\t{app}\t{module}\t{message}".format(date=log["date"], time=log["time"], type=log["type"], app=log["logger"], module=log["module"], message=log["message"])
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
        print(data)
    except Exception as e:
        print(e)

if __name__ == '__main__':
    config = Properties()
    with open('resources/app.properties','rb') as app_properties:
        config.load(app_properties,"utf-8")
    cli()