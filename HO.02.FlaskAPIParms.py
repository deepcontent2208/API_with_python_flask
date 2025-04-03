from flask import Flask, request

app = Flask(__name__)

@app.route('/listproducts/')
def listProduct():
    with open('retail_product_data.csv') as ifile:
        lines = ifile.readlines()
    return lines


@app.route('/productdetail/<int:pid>/<string:column>')
def productDetail(pid, column):
    product_id = pid
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


from flask import request

@app.route('/productdetail/price')
@app.route('/productdetail/qty')
@app.route('/productdetail/category')
@app.route('/productdetail/supplier')
@app.route('/productdetail/created')

def selectProductCols():
    url = request.url
    url = url.split('/')[-1]
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


@app.route('/listamount')
def listAmount2():
    products = dict()
    product_list = list()
    with open('retail_product_data.csv') as ip_file:
        lines = ip_file.readlines()
        for line in lines:
            product_id = line.split(',')[0]
            product_name = line.split(',')[1]
            product_price = line.split(',')[3]
            function_name = "listAmount2 - 2nd function"
            products["product_id"] = product_id
            products["product_name"] = product_name
            products["product_price"] = product_price
            products["function_name"] = function_name
            product_list.append(products.copy())

        return product_list

@app.route('/listamount')
def listAmount1():
    with open('retail_product_data.csv') as ip_file:
        lines = ip_file.readlines()
        products = dict()
        product_list = list()
        for line in lines:
            product_id = line.split(',')[0]
            product_name = line.split(',')[1]
            product_price = line.split(',')[3]
            function_name = "listAmount1 - 1st function"
            products["product_id"] = product_id
            products["product_name"] = product_name
            products["product_price"] = product_price
            products["function_name"] = function_name
            product_list.append(products.copy())

    return product_list


@app.route('/productdetail/<product_id>/price')
def productLevelCols(product_id):
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
                elif url == "qty":
                    data["product_id"] = file_product_id
                    data["price"] = i.split(',')[3]
                    data["quantity"] = i.split(',')[5]
                else:
                    data["msg"] = "Please provide a valid column - price or qty"
                break
            else:
                data["msg"] = "Product not found!!"


if __name__ == "__main__":
    app.run(host='0.0.0.0',port=8000,debug=True)