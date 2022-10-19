from flask import Flask, jsonify, request
from flask_restful import Resource, Api
import sql_connection

app = Flask(__name__)
api = Api(app)

class insert_log():
    def post(self):
        json_data = request.get_json(force=True)
        full_date = json_data['full_date']
        type = json_data ['type']
        message = json_data['message']
        sql_connection.insert_log(full_date, type, message)
        return jsonify(full_date = full_date, type = type, message = message)

api.add_resource(insert_log, '/insert_log')

class get_logs():
    def get(self):
        return(sql_connection.get_logs())

api.add_resource(get_logs, '/get_logs')
