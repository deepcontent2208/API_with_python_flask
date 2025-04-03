from flask import Flask

app = Flask(__name__)

@app.route('/listproduct')
def listProduct():
    with open('retail_product_data.csv') as product_file:
        lines = product_file.readlines()
        items = dict()
        items_list = list()
        for i in lines:
            items['product_id'] = i.split(',')[0]
            items['product_name'] = i.split(',')[1]
            items_list.append(items.copy())

    return items_list


@app.route('/listpriceqty')
def listPriceQty():
    with open('retail_product_data.csv') as product_file:
        lines = product_file.readlines()
        items = dict()
        items_list = list()
        for i in lines:
            items['product_id'] = i.split(',')[0]
            items['price'] = i.split(',')[3]
            items['quantity'] = i.split(',')[5]
            items_list.append(items.copy())

    return items_list


if __name__ == "__main__":
    app.run(host='0.0.0.0',port=8000,debug=True)
    # listProduct()