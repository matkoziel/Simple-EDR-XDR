from flask import Flask, jsonify, request
from flask_restful import Resource, Api
import sql_connection
import time

class insert_log(Resource):
    def post(self):
        json_data = request.get_json()
        logger = json_data['name']
        type = json_data['levelname']
        msg = json_data['msg']
        module = json_data['filename'] + '.' + json_data['module']
        date = int(float(json_data["created"])*1000)
        datef = (time.strftime('%d/%m/%Y %H:%M:%S:{}'.format(date%1000), time.gmtime(date/1000.0)))
        dmy = datef.split(" ")[0]
        hms = datef.split(" ")[1]
        sql_connection.insert_log(type, dmy, hms, logger, module, msg)
        return jsonify(type = type, date = dmy, time = hms, source = logger, module = module, message = msg)

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