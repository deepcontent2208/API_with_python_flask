from flask import Flask, request


app = Flask(__name__)

@app.route('/getcustdata', methods=['GET'])
def get_cust_data():
    customer_id = request.args['cust_id']
    customer_id = str(customer_id)
    data = dict()
    found = 'N'
    print(customer_id)

    with open('finance_customer_data.csv') as customer_file:
        lines = customer_file.readlines()
        for line in lines:
            file_cust_id = line.split(',')[0]

            if customer_id == file_cust_id:
                print('inside of file loop : ',file_cust_id,customer_id)
                data['data'] = line
                found = 'Y'
                break

        if found == 'N':
            data['msg'] = 'customer not found'

    return data


if __name__ == "__main__":
    app.run(host='0.0.0.0',port=8000,debug=True)
