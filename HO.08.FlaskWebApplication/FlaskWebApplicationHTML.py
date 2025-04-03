from flask import Flask, request, render_template
import pymysql

app = Flask(__name__)

def connect_to_db():
    conn = pymysql.connect(
        host="<aurora-mysql-endpoint>",
        user="admin",
        password="xxxx",
        database="financedb"
    )
    return conn


@app.route("/", methods=['GET'])
def main_page():
    return render_template("main_page.html")


@app.route('/getcustaccts', methods=['GET'])
def get_cust_accts():
    item_list = list()
    data = dict()
    cust_id = request.args["cust_id"]
    cursor = conn.cursor()
    sql = "SELECT customer_id, account_id, account_type, balance FROM accounts WHERE customer_id = %s"
    cursor.execute(sql,cust_id)

    records = cursor.fetchall()
    item_list = records

    return render_template("customer_details_page.html",
                           array_data=item_list, cust_id=cust_id)


@app.route('/getacctdetails', methods=['GET'])
def get_acct_details():
    acct_id = request.args["acct_id"]
    cursor = conn.cursor()
    sql = "SELECT * FROM accounts WHERE account_id = %s"
    cursor.execute(sql, acct_id)
    row = cursor.fetchone()

    acct_bal = row[3]
    account_type = row[1]
    currency_code = row[4]
    acc_opening_date = row[5]
    last_update_date = row[6]

    return render_template("account_details_page.html",
                           acct_id=acct_id,
                           acct_bal=acct_bal,
                           account_type=account_type,
                           currency_code=currency_code,
                           acc_opening_date=acc_opening_date,
                           last_update_date=last_update_date)


if __name__ == "__main__":
    global conn
    conn = connect_to_db()
    app.run(host='0.0.0.0',port=8000,debug=True)