from flask import Flask, url_for, request
import pymysql

app = Flask(__name__)

def connect_to_db():
    conn = pymysql.connect(
        host="python-flask-aurora-mysql.cluster-c7qm6ay60wsi.ap-south-1.rds.amazonaws.com",
        user="admin",
        password="Deepcontent2208",
        database="crmdb"
    )
    return conn


@app.route('/completeassemblyline', methods=['PUT'])
def complete_assembly_line():
    pass

if __name__ == "__main__":
    global conn
    conn = connect_to_db()
    app.run(host='0.0.0.0',port=10000,debug=True)