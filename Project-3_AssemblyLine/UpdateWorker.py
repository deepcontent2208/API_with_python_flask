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


@app.route('/updateworker', methods=['POST'])
def update_worker():
    assigned_ws_id = request.args.get('assigned_ws_id')
    output_data = dict()

    cursor = conn.cursor()
    get_worker_sql = 'SELECT worker_id FROM worker WHERE assigned_ws_id = %s AND is_available ="Y"'
    cursor.execute(get_worker_sql,assigned_ws_id)
    worker_id = cursor.fetchone()

    if worker_id:
        cursor.close()
        worker_id = cursor.fetchone()[0]
        output_data['worker_id'] = worker_id
        cursor = conn.cursor()
        update_worker_sql = 'UPDATE worker SET is_available = "N" WHERE worker_id = %s '
        cursor.execute(update_worker_sql, worker_id)
        cursor.close()
        conn.commit()
    else:
        output_data['worker_id'] = "ERROR"
        cursor.close()

    conn.commit()
    return output_data


if __name__ == "__main__":
    global conn
    conn = connect_to_db()
    app.run(host='0.0.0.0',port=12000,debug=True)