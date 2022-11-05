from flask import Flask, jsonify, request, send_file
from flask_restful import Resource, Api

import logs
import network
import remote_control

class execute_command(Resource):
    def post(self):
        json_data = request.form
        output = remote_control.execute_command(json_data['command'])
        return jsonify(command = json_data['command'], output = output)

class get_log_list(Resource):
    def get(self):
        return logs.get_logs()

class get_chosen_logs(Resource):
    def get(self):
        print('to do')

class get_network_config(Resource):
    def get(self):
        return network.get_network_config()

class get_pcaps_list(Resource):
    def get(self):
        return network.get_pcaps()

class get_chosen_pcaps(Resource):
    def get(self):
        print('to do')

class sniffing(Resource):
    def post(self):
        json_data = request.form
        interface = json_data['interface']
        filter = json_data['filter']
        file_name = json_data['file_name']
        sniff_time = json_data['sniff_time']
        network.sniff(interface, filter, file_name, sniff_time)
        return jsonify(interface = interface, filter = filter, file_name = file_name, sniff_time = sniff_time)


if __name__ == '__main__':
    app = Flask(__name__)
    api = Api(app)
    api.add_resource(execute_command, '/execute_command')
    api.add_resource(get_log_list, '/get_log_list')
    api.add_resource(get_chosen_logs, '/get_chosen_logs')
    api.add_resource(get_network_config, '/get_network_config')
    api.add_resource(get_pcaps_list, '/get_pcaps_list')
    api.add_resource(get_chosen_pcaps, '/get_chosen_pcaps')
    api.add_resource(sniffing, '/sniffing')
    app.run(host='0.0.0.0', port = 3000, debug=True)