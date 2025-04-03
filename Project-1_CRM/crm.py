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


@app.route('/cust/<cust_id>', methods=['GET'])
@app.route('/cust/<cust_id>/loans', methods=['GET'])
@app.route('/cust/<cust_id>/loan/<loan_id>', methods=['GET'])
@app.route('/cust/<cust_id>/accs', methods=['PATCH'])
@app.route('/cust/<cust_id>/acc/<acc_id>', methods=['PATCH'])
@app.route('/cust/noloans', methods=['PATCH'])
def crm_cust_lookup(cust_id=0, loan_id=0, acc_id=0):
    base_url = request.url
    base_url = base_url.split('/')

    if base_url[-2] == 'cust' and base_url[-1] != 'noloans':
        data = dict()
        sql = "SELECT * FROM customers WHERE customer_id = %s"
        cursor = conn.cursor()
        cursor.execute(sql,cust_id)
        record = cursor.fetchone()
        data["customer_id"] = record[0]
        data["first_name"] = record[1]
        data["last_name"] = record[2]
        data["email"] = record[3]

    elif base_url[-1] == 'loans':
        sql = "SELECT customer_id, loan_id FROM loans WHERE customer_id = %s"
        cursor = conn.cursor()
        cursor.execute(sql, cust_id)
        records = cursor.fetchall()
        if len(records) == 0:
            data = "no loans for this customer"
        else:
            data = list()
            for record in records:
                data.append(record)

    elif base_url[-2] == 'loan':
        data = dict()
        sql = "SELECT * FROM loans WHERE loan_id = %s"
        cursor = conn.cursor()
        cursor.execute(sql, loan_id)
        record = cursor.fetchone()
        if len(record) > 0:
            data["loan_id"] = record[0]
            data["loan_type"] = record[2]
            data["principal_amount"] = record[3]
            data["interest_rate"] = record[4]
            data["term_month"] = record[5]
            data["loan_start_date"] = record[6]
            data["loan_end_date"] = record[7]
        else:
            data["msg"] = "no loan information for this loan account"

    elif base_url[-1] == 'accs':
        sql = "SELECT account_id, balance FROM accounts WHERE customer_id = %s"
        cursor = conn.cursor()
        cursor.execute(sql, cust_id)
        records = cursor.fetchall()
        if len(records) == 0:
            data = "no loans for this customer"
        else:
            data = list()
            for record in records:
                data.append(record)

    elif base_url[-2] == 'acc':
        data = dict()
        sql = "SELECT account_id, balance, currency_code, acc_opening_date FROM accounts WHERE account_id = %s"
        cursor = conn.cursor()
        cursor.execute(sql, acc_id)
        record = cursor.fetchone()
        data["account_id"] = record[0]
        data["account_bal"] = record[1]
        data["currency_code"] = record[2]
        data["acc_opening_date"] = record[3]

    elif base_url[-1] == 'noloans':
        sql = "SELECT distinct(customer_id) FROM customers EXCEPT SELECT distinct(customer_id) FROM loans"
        cursor = conn.cursor()
        cursor.execute(sql)
        records = cursor.fetchall()
        if len(records) == 0:
            data = "no loans for any customer"
        else:
            data = list()
            for record in records:
                data.append(record)

    return data


if __name__ == "__main__":
    global conn
    conn = connect_to_db()
    app.run(host='0.0.0.0',port=10000,debug=True)


