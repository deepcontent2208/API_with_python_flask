from flask import Flask, url_for, request
import pymysql

app = Flask(__name__)

def connect_to_db():
    conn = pymysql.connect(
        host="python-flask-aurora-mysql.cluster-c7qm6ay60wsi.ap-south-1.rds.amazonaws.com",
        user="admin",
        password="Deepcontent2208",
        database="assembly_line_db"
    )
    return conn


@app.route('/updatemachine', methods=['PUT'])
def update_machine():
    ws_id = request.args.get('ws_id')
    output_data = dict()

    get_machine_sql = 'SELECT machine_id FROM machine WHERE is_available = "Y"'
    cursor = conn.cursor()
    cursor.execute(get_machine_sql)
    machine_id = cursor.fetchone()

    if machine_id:
        machine_id = cursor.fetchone()[0]
        cursor.close()
        update_machine_sql = 'UPDATE machine SET is_available = "N", ws_id = %s WHERE machine_id = %s'
        cursor = conn.cursor()
        cursor.execute(update_machine_sql, (ws_id, machine_id))
        cursor.close()
        output_data['machine_id'] = machine_id
    else:
        output_data['machine_id'] = "ERROR"
        cursor.close()

    conn.commit()
    return output_data

if __name__ == "__main__":
    global conn
    conn = connect_to_db()
    app.run(host='0.0.0.0',port=13000,debug=True)