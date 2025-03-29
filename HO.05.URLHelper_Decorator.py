
#########################################################################################
# Flask URL Helper Functions
#########################################################################################
from flask import Flask, redirect, abort

# app = Flask(__name__)

def listProduct():
    with open('retail_product_data.csv') as product_file:
        lines = product_file.readlines()
        items = dict()
        items_list = list()
        for i in lines:
            items['product_id'] = i.split(',')[0]
            items['product_name'] = i.split(',')[1]
            items_list.append(items.copy())
    # return redirect('/listpriceqty')
    # return items_list
    abort(504)


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
    # return redirect('/listproduct')


# app.add_url_rule('/listproduct', view_func=listProduct)
# app.add_url_rule('/listpriceqty', view_func=listPriceQty)

#########################################################################################
# Python Decorators
#########################################################################################
def decorate_listProduct(func):
    print('func: decorate_listProduct')
    def listProductDetail():
        print('func: listProductDetail')
        items = dict()
        with open('retail_product_data.csv') as product_file:
            lines = product_file.readlines()
            for line in lines:
                items['product_id'] = line.split(',')[0]
                items['product_qty'] = line.split(',')[5]
                items['product_supplier'] = line.split(',')[6]
                item_list.append(items.copy())
        return func()
    return listProductDetail


@decorate_listProduct
def listProduct():
    print('func: listProduct')
    with open('retail_product_data.csv') as product_file:
        lines = product_file.readlines()
        items = dict()
        for i in lines:
            items['product_id'] = i.split(',')[0]
            items['product_name'] = i.split(',')[1]
            items['product_price'] = i.split(',')[3]
            item_list.append(items.copy())
    return item_list

# listProduct = decorate_listProduct(listProduct)

if __name__ == "__main__":
    print('func: __main__')
    global item_list
    item_list = list()
    products = listProduct()
    for row in products:
        print(row)
    # app.run(host='0.0.0.0',port=8000,debug=True)
    # products = listProduct
    # print(listProduct())
    # print(listProduct)
    # print(products)
    # print(products())
