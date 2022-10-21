import click
import requests
from jproperties import Properties

@click.group()
def cli():
    pass

@cli.group('parse_log')
def parse_log():
    pass

@parse_log.command('use_re')
@click.option('-r','--regex',default='', type=click.STRING)
@click.option('-p','--path',type=click.File('r'),required=True)
def use_re(regex,file):
    click.echo(regex + str(file))

@parse_log.command('use_grep')
@click.option('-r','--regex',default='', type=click.STRING)
@click.option('-p','--path',type=click.File('r'),required=True)
def use_grep(regex,file):
    click.echo(regex + str(file))

@cli.group('show_pcap')
def show_pcap():
    pass

@show_pcap.command('use_libpcap')
@click.option('-p','--path',type=click.File('r'))
@click.option('-f','--filter',default='', type=click.STRING)
def use_libpcap(path, filter):
    click.echo(str(path) + filter)

@show_pcap.command('use_tshark')
@click.option('-p','--path',type=click.File('r'),required=True)
@click.option('-f','--filter',default='', type=click.STRING)
def use_libpcap(path, filter):
    click.echo(str(path) + filter)

@cli.group('remote_logger')
def remote_logger():
    pass

@remote_logger.command('get_logs')
@click.option('-s','--start',type=click.STRING)
@click.option('-e','--end',type=click.STRING)
def get_logs(start,end):
    if start and not end:
        #TODO: REST API for parametrized request
        pass
    elif end and not start:
        #TODO: REST API for parametrized request
        pass
    elif start and end:
        #TODO: REST API for parametrized request
        pass
    else:
        host=config.get('REMOTE_LOGGER_HOST').data
        port=config.get('REMOTE_LOGGER_PORT').data
        uri="http://{host}:{port}/get_logs".format(host=host,port=port)
        resposne = requests.get(url=uri)
        data = resposne.json()
        print(data)


if __name__ == '__main__':
    config = Properties()
    with open('resources/app.properties','rb') as app_properties:
        config.load(app_properties,"utf-8")
    cli()