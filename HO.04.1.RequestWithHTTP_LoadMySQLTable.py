import pymysql

conn = pymysql.connect(
       host="<get-the-endpoint-from-rds-console>",
       user="admin",
       password="<your-password>",
       database="financedb"
)
cursor = conn.cursor()
sql = "INSERT INTO customer VALUES (%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s)"

with open('finance_customer_data.csv') as ifile:
    lines = ifile.readlines()
    for record in lines:
        # print(record)
        customer_id, first_name, last_name, email, phone_number, date_of_birth, gender, national_id, address_line_1, address_line_2, city, country, postal_code, created_at, updated_at = record.strip().split(',')
        # print(customer_id, first_name, last_name, email, phone_number, date_of_birth, gender, national_id, address_line_1, address_line_2, city, country, postal_code, created_at, updated_at)
        cursor.execute(sql,(customer_id, first_name, last_name, email, phone_number, date_of_birth, gender, national_id, address_line_1, address_line_2, city, country, postal_code, created_at, updated_at))

conn.commit()
conn.close()