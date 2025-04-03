from flask import Flask, request

app = Flask(__name__)


@app.route('/listproducts/')
def listProduct():
    with open('retail_product_data.csv') as ifile:
        lines = ifile.readlines()
    return lines


@app.route('/productdetail/<int:pid>')
def productDetail(pid):
    product_id = str(pid)
    data = dict()
    with open('retail_product_data.csv') as product_file:
        lines = product_file.readlines()
        for i in lines:
            data = dict()
            file_product_id = i.split(',')[0]
            print(file_product_id)
            if file_product_id == product_id:
                data["product_id"] = file_product_id
                data["price"] = i.split(',')[3]
                data["quantity"] = i.split(',')[5]
                data["supplier"] = i.split(',')[6]
            else:
                data["msg"] = "Product not found!!"

    return data


if __name__ == "__main__":
    app.run(host='0.0.0.0',port=8000,debug=True)