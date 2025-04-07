from flask import Flask, url_for, request
import pymysql, requests, json


app = Flask(__name__)

def connect_to_db():
    conn = pymysql.connect(
        host="python-flask-aurora-mysql.cluster-c7qm6ay60wsi.ap-south-1.rds.amazonaws.com",
        user="admin",
        password="Deepcontent2208",
        database="assembly_line_db"
    )
    return conn


@app.route('/getws', methods=['GET'])
def get_workstation():
    bay_id = request.args['ws_bay_id']
    output_record = dict()

    cursor = conn.cursor()
    get_ws_sql = 'SELECT ws_id, next_ws_id FROM workstation WHERE ws_bay_id = %s AND is_available = "Y"'
    cursor.execute(get_ws_sql,bay_id)
    record = cursor.fetchone()

    if record:
        assigned_ws_id = record[0]
        next_ws_id = record[1]
        parm = {'assigned_ws_id' : assigned_ws_id}
        worker_id = requests.post('http://127.0.0.1:12000/updateworker', params=parm)

        if worker_id.status_code == 200:
            try:
                worker_id = worker_id.json()['worker_id']
                cursor = conn.cursor()
                update_ws_sql = 'UPDATE workstation SET is_available = "N" WHERE ws_id = %s'
                cursor.execute(update_ws_sql, assigned_ws_id)
                cursor.close()
                output_record['worker_id'] = worker_id
                output_record['next_ws_id'] = next_ws_id
                output_record['ws_id'] = assigned_ws_id

            except KeyError:
                print("HTTP 200 Pgm: UpdateWorkStation. Function: getws. Msg: Worker not found!!")
                output_record["msg"] = "No worker found. Please try a different Workstation"
                output_record['ws_id'] = "ERROR"
                output_record['worker_id'] = "ERROR"
                output_record['next_ws_id'] = "ERROR"

        else:
            print("HTTP Non200 Pgm: UpdateWorkStation. Function: getws. Msg: Worker not found!!")
            output_record["msg"] = "No worker found. Please try a different Workstation"
            output_record['ws_id'] = "ERROR"
            output_record['worker_id'] = "ERROR"
            output_record['next_ws_id'] = "ERROR"

    else:
        output_record['msg'] = 'Workstation not found. Try another Bay ID.'
        output_record['ws_id'] = 'ERROR'
        output_record['worker_id'] = "ERROR"
        output_record['next_ws_id'] = "ERROR"

    conn.commit()
    return output_record


@app.route('/updatews', methods=['POST'])
def update_workstation():
    pass


if __name__ == "__main__":
    global conn
    conn = connect_to_db()
    app.run(host='0.0.0.0',port=11000,debug=True)