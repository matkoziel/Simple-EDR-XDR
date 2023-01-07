from flask import Flask, jsonify, request
from flask_restful import Resource, Api
import sql_connection
import time

class insert_log(Resource):
    def post(self):
        json_data = request.get_json()
        rule_name = json_data['rule_name']
        msg = json_data['msg']
        timestamp = json_data['timestamp']
        sql_connection.insert_log(timestamp, rule_name, msg)
        return jsonify(timestamp = timestamp, rule_name = rule_name, message = msg)

class get_logs(Resource):
    def get(self):
        return(sql_connection.get_logs())

class get_specific_logs(Resource):
    def get(sefl):
        json_data = request.get_json()
        query = json_data['filter']
        return(sql_connection.get_specific_logs(query))

if __name__ == '__main__':
    app = Flask(__name__)
    api = Api(app)
    sql_connection.init()
    api.add_resource(insert_log, '/insert_log')
    api.add_resource(get_logs, '/get_logs')
    api.add_resource(get_specific_logs, '/get_specific_logs')
    
    app.run(host='0.0.0.0', port = 3000, debug=True)