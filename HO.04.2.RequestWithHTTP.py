from flask import Flask, request
import pymysql

app = Flask(__name__)

def connect_to_database():
    conn = pymysql.connect(
        host="<aurora-endpoint>",
        user="admin",
        password="xxxx",
        database="financedb"
    )
    return conn

@app.route("/getcustdetail", methods=['GET'])
def get_cust_details():
    data = dict()
    dbconn = connect_to_database()
    cursor = dbconn.cursor()

    cust_id = request.args["cust_id"]
    sql = "select * from customer where customer_id = %s"
    cursor.execute(sql,cust_id)

    records = cursor.fetchall()
    for row in records:
        data["customer_id"] = row[0]
        data["first_name"] = row[1]
        data["last_name"] = row[2]
        data["email"] = row[3]
        data["phone_number"] = row[4]

    return data

@app.route("/listcustomers", methods=['GET'])
def list_customers():
    pass


@app.route("/addcustomer", methods=['PUT'])
def add_customer():
    from datetime import datetime
    customer_id = request.json["customer_id"]
    first_name = request.json["first_name"]
    last_name = request.json["last_name"]
    email = request.json["email"]
    phone_number = request.json["phone_number"]
    date_of_birth = request.json["date_of_birth"]
    gender = request.json["gender"]
    national_id = request.json["national_id"]
    address_line_1 = request.json["address_line_1"]
    address_line_2 = request.json["address_line_2"]
    city = request.json["city"]
    country = request.json["country"]
    postal_code = request.json["postal_code"]
    created_at = datetime.now()
    updated_at = datetime.now()

    data = dict()
    dbconn = connect_to_database()
    cursor = dbconn.cursor()

    sql = "INSERT INTO customer VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    try:
        cursor.execute(sql,(customer_id,first_name,last_name,email,
                                 phone_number,date_of_birth,gender,national_id,
                                 address_line_1,address_line_2,city,country,
                                 postal_code,created_at,updated_at))
        dbconn.commit()
    except Exception as e:
        data["msg"] = "INSERT records to customer table failed!!!"
    else:
        data["msg"] = "INSERT records to customer table successful!!!"

    return data


@app.route("/updatecustomer", methods=['POST'])
def update_customer():
 pass

@app.route("/deletecustomer", methods=['DELETE'])
def delete_customer():
    pass

@app.route("/upsertcustomer", methods=['GET','PUT','POST'])
def upsert_customer():
    if request.method == "GET":
        pass
    elif request.method == "PUT":
        pass
    elif request.method == "POST":
        pass


if __name__ == "__main__":
    app.run(host='0.0.0.0',port=8000,debug=True)