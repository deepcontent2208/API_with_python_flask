from flask import Flask, request

app = Flask(__name__)


@app.route('/productdetail')
def productDetail():
    url_args = request.args
    data = dict()
    data['var1'] = url_args['product_id']
    data['var2'] = url_args['column']
    data['var3'] = url_args['name']
    # data = request.values
    return data

    data = dict()
    with open('retail_product_data.csv') as product_file:
        lines = product_file.readlines()
        for i in lines:
            data = dict()
            file_product_id = i.split(',')[0]
            if file_product_id == product_id:
                if column == "price":
                    data["product_id"] = file_product_id
                    data["price"] = i.split(',')[3]
                elif column == "qty":
                    data["product_id"] = file_product_id
                    data["price"] = i.split(',')[3]
                    data["quantity"] = i.split(',')[5]
                else:
                    data["msg"] = "Please provide a valid column - price or qty"
                break
            else:
                data["msg"] = "Product not found!!"

    return data


@app.route('/productdetail/<product_id>/price/<name>/qty')
def productLevelCols(product_id, name):
    url = request.url.split('/')[-1]
    with open('retail_product_data.csv') as product_file:
        lines = product_file.readlines()
        for i in lines:
            data = dict()
            file_product_id = i.split(',')[0]
            if file_product_id == product_id:
                if url == "price":
                    data["product_id"] = file_product_id
                    data["price"] = i.split(',')[3]
                    data["name"] = name
                elif url == "qty":
                    data["product_id"] = file_product_id
                    data["price"] = i.split(',')[3]
                    data["quantity"] = i.split(',')[5]
                    data["name"] = name
                else:
                    data["msg"] = "Please provide a valid column - price or qty"
                break
            else:
                data["msg"] = "Product not found!!"

    return data



if __name__ == "__main__":
    app.run(host='0.0.0.0',port=8000,debug=True)