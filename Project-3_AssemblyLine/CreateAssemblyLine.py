from itertools import product
from datetime import date, datetime
import uuid

from flask import Flask, url_for, request
import pymysql, requests, random

app = Flask(__name__)

def connect_to_db():
    conn = pymysql.connect(
        host="python-flask-aurora-mysql.cluster-c7qm6ay60wsi.ap-south-1.rds.amazonaws.com",
        user="admin",
        password="Deepcontent2208",
        database="assembly_line_db"
    )
    return conn


@app.route('/createassemblyline', methods=['GET'])
def create_assembly_line():
    product_name = request.args['product_name']
    bay_id = request.args['bay_id']
    output_data = dict()

    parm = {"ws_bay_id" : bay_id}
    ws_ids = requests.get('http://127.0.0.1:11000/getws',params=parm)

    if ws_ids.status_code == 200:
        record = ws_ids.json()
        try:
            ws_id = record['ws_id']
        except KeyError:
            print("HTTP 200 Pgm: CreateAssemblyLine. Function: create_assembly_line. Msg: Workstation not found!!")
            output_data['msg'] = ws_ids.json()['msg']
            output_data['ws_id'] = ws_ids.json()['ws_id']
            ws_id = ws_ids.json()['ws_id']
        else:
            ws_id = record['ws_id']
            worker_id = record['worker_id']
    else:
        print("HTTP Non200 Pgm: CreateAssemblyLine. Function: create_assembly_line. Msg: Workstation not found!!")
        output_data['msg'] = ws_ids.json()['msg']
        output_data['ws_id'] = ws_ids.json()['ws_id']
        ws_id = ws_ids.json()['ws_id']
    print('ws_id :', ws_id)
    print(output_data)
    if ws_id == "ERROR":
        output_data['msg'] = ws_ids.json()['msg']
        output_data['ws_id'] = ws_ids.json()['ws_id']
    else:
        machine_id = requests.put('http://127.0.0.1:13000/updatemachine', params=ws_id)

        if machine_id.status_code == 200:
            try:
                mc_id = machine_id.json()['machine_id']
            except KeyError:
                output_data['msg'] = 'No machine found for Workstation. Try another Bay.'
            else:
                mc_found = 'Y'
        else:
            output_data['msg'] = 'No machine found for Workstation. Try another Bay.'

        if mc_found == 'Y':
            line_id = random.randint(2200,33000)
            product_id = random.randint(11111111,99999999)
            name = product_name
            status = "started"
            start_ws_id = ws_id
            current_ws_id = ws_id
            end_ws_id = 'NOT YET ASSIGNED'
            start_time = datetime.now()
            end_time = "9999-99-99"
            log_id = str(uuid.uuid4())

            cursor = conn.cursor()
            assembly_line_entry_sql = "INSERT INTO assembly_line VALUES (%s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(assembly_line_entry_sql,(line_id, product_id, name, start_ws_id, current_ws_id, end_ws_id, status))
            cursor.close()

            output_data["line_id"] = line_id
            output_data["product_id"] = product_id
            output_data["product_name"] = name
            output_data["status"] = status
            output_data["start_ws_id"] = start_ws_id
            output_data["end_ws_id"] = end_ws_id
            output_data["start_time"] = start_time
            output_data["end_time"] = end_time
            output_data["log_id"] = log_id

            cursor = conn.cursor()
            production_log_entry_sql = 'INSERT INTO production_log VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'
            cursor.execute(production_log_entry_sql, (log_id, product_id, start_ws_id, worker_id, mc_id, start_time, end_time, status))
            conn.commit()
            cursor.close()
        else:
            output_data['msg'] = 'No machine found for Workstation. Try another Bay.'

    return output_data


if __name__ == "__main__":
    global conn
    conn = connect_to_db()
    app.run(host='0.0.0.0',port=10000,debug=True)


