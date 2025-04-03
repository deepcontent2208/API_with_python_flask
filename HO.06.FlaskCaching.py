from flask import Flask, request
import pymysql
from flask_caching import Cache

app = Flask(__name__)
cache = Cache(config={'CACHE_TYPE': 'SimpleCache'})
cache.init_app(app)

def connect_to_database():
    conn = pymysql.connect(
        host="<Aurora Endpoint>",
        user="admin",
        password="Password",
        database="financedb"
    )
    return conn


@app.route("/getcustdetails")
def get_cust_details():
    conn = connect_to_database()
    cursor = conn.cursor()
    cust_id = request.args['cust_id']

    sql = "SELECT * FROM customer WHERE customer_id = %s"
    cursor.execute(sql, cust_id)
    data = dict()
    item_list = list()

    records = cursor.fetchall()
    for record in records:
        data["customer_id"] = record[0]
        data["first_name"] = record[1]
        data["last_name"] = record[2]
        data["email"] = record[3]
        data["phone_number"] = record[4]
        data["dob"] = record[5]
        data["gender"] = record[6]
        data["national_id"] = record[7]
        data["address_line_1"] = record[8]
        data["address_line_1"] = record[9]
        data["city"] = record[10]
        data["country"] = record[11]
        data["postal_code"] = record[12]
        data["created_at"] = record[13]
        data["created_at"] = record[14]
        item_list.append(data.copy())

    return item_list


@app.route("/getcustdetailscached/<cust_id>")
@cache.cached()
# @cache.cached(timeout=30)
def get_cust_details_cached(cust_id):
    conn = connect_to_database()
    cursor = conn.cursor()
    # cust_id = request.args['cust_id']

    sql = "SELECT * FROM customer WHERE customer_id = %s"
    cursor.execute(sql, cust_id)
    data = dict()
    item_list = list()

    records = cursor.fetchall()
    for record in records:
        data["customer_id"] = record[0]
        data["first_name"] = record[1]
        data["last_name"] = record[2]
        data["email"] = record[3]
        data["phone_number"] = record[4]
        data["dob"] = record[5]
        data["gender"] = record[6]
        data["national_id"] = record[7]
        data["address_line_1"] = record[8]
        data["address_line_1"] = record[9]
        data["city"] = record[10]
        data["country"] = record[11]
        data["postal_code"] = record[12]
        data["created_at"] = record[13]
        data["created_at"] = record[14]
        item_list.append(data.copy())

    return item_list


@app.route("/clearcache")
def clear_cache():
    cache.clear()
    return "cache cleared"


@app.route("/cacheadmin")
def cache_admin():
    with open('finance_customer_master_data.csv') as admin_file:
        lines = admin_file.readlines()
        for line in lines:
            cache.set("admin_data",line)
    return "Admin data cached"


@app.route("/getcachedadmin")
def get_cached_admin():
    admin_data = cache.get("admin_data")
    return admin_data


if __name__ == "__main__":
    app.run(host='0.0.0.0',port=8000,debug=True)



























