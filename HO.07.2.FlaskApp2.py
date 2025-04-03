from flask import Flask, request

app = Flask(__name__)

from flask import request

@app.route('/productdetail/price')
@app.route('/productdetail/qty')
@app.route('/productdetail/category')
@app.route('/productdetail/supplier')
@app.route('/productdetail/created')

def selectProductCols():
    url = request.url
    url = url.split('/')[-1]
    print(url)
    product_list = list()
    products = dict()
    with open('retail_product_data.csv') as ip_file:
        lines = ip_file.readlines()
        for line in lines:
            product_id = line.split(',')[0]
            product_name = line.split(',')[1]
            if url == "price":
                product_col = line.split(',')[3]
            elif url == "category":
                product_col = line.split(',')[2]
            elif url == 'qty':
                product_col = line.split(',')[5]
            elif url == 'supplier':
                product_col = line.split(',')[6]
            elif url == 'created':
                product_col = line.split(',')[7]
            else:
                product_col = "please select the correct column"

            products["product_id"] = product_id
            products["product_name"] = product_name
            products[url] = product_col

            product_list.append(products.copy())


    return product_list


if __name__ == "__main__":
    app.run(host='0.0.0.0',port=8001,debug=True)