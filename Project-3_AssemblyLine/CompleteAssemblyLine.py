from flask import Flask, url_for, request
import pymysql

app = Flask(__name__)


@app.route('/completeassemblyline', methods=['PUT'])
def complete_assembly_line():
    pass

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=10000,debug=True)