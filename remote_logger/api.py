from flask import Flask, jsonify, request
from flask_restful import Resource, Api
import sql_connection

class insert_log(Resource):
    def post(self):
        json_data = request.get_json(force=True)
        full_date = json_data['full_date']
        type = json_data ['type']
        message = json_data['message']
        sql_connection.insert_log(full_date, type, message)
        return jsonify(full_date = full_date, type = type, message = message)

class get_logs(Resource):
    def get(self):
        return(sql_connection.get_logs())

def start_api():
    app = Flask(__name__)
    api = Api(app)
    api.add_resource(insert_log, '/insert_log')
    api.add_resource(get_logs, '/get_logs')
    app.run()