from flask import Flask
from flask import render_template
from flask import request

import database_adapter as db
import json

app = Flask(__name__)

# methods can be called by entering specific url in browser
# rather by calls from html elements, in final version


# returns main html page
@app.route('/')
def root():
    return render_template("client.html")


# initializes the database
@app.route('/init_db')
def init_db():
    db.init()
    return "Database Initialized"


# returns all storage city names
@app.route('/get_storages')
def get_storages():
    storages = db.get_storages()
    if storages is not None:
        return create_response_data(True, "Storages retrieved", storages)
    else:
        return create_response(False, "Failed to retrieve storages")


# returns city name of the storage with called id
@app.route("/get_storage_by_id/<storage_id>")
def get_storage_by_id(storage_id):
    data = db.get_storage_by_id(storage_id)
    if data is not None:
        return create_response_data(True, "Storage_retrieved", data)
    else:
        return create_response(False, "No such storage")


# returns the name of the product with called id
@app.route("/get_product_by_id/<product_id>")
def get_product_by_id(product_id):
    data = db.get_product_by_id(product_id)
    if data is not None:
        return create_response_data(True, "Product_retrieved", data)
    else:
        return create_response(False, "No such product")


# returns the stock(s) with called storage name
@app.route("/get_stock_by_storage_name/<storage_name>")
def get_stock_by_storage_name(storage_name):
    data = db.get_stock_by_storage_name(storage_name)
    if data is not None:
        return create_response_data(True, "Stock retrieved", data)
    else:
        return create_response(False, "No such stock")


# returns the io(s) with called storage name
@app.route("/get_io_by_storage_name/<storage_name>")
def get_io_by_storage_name(storage_name):
    data = db.get_io_by_storage_name(storage_name)
    if data is not None:
        return create_response_data(True, "IO retrieved", data)
    else:
        return create_response(False, "No such IO")


# adds io shipment
@app.route("/add_io/", methods=['POST'])
def add_io():
    data = json.loads(unicode(request.data, "UTF-8"))
    ship_date = data[0]['date']
    product_name = data[0]['product']
    storage_name = data[0]['storage']
    ship_amount = data[0]['amount']
    if db.add_io(ship_date, product_name, storage_name, ship_amount):
        return create_response(True, "io created")
    else:
        return create_response(False, "Failed to create io")


# adds stock
@app.route("/add_stock/<product_name>/<storage_name>/<current_balance>")
def add_stock(product_name, storage_name, current_balance):
    if db.add_stock(product_name, storage_name, current_balance):
        return create_response(True, "stock created")
    else:
        return create_response(False, "Failed to create stock")


# creates a JSON response with additional data
def create_response_data(success, message, data):
    print message
    return json.dumps({'success': success, 'message': message, 'data': data})


# creates a JSON response
def create_response(success, message):
    print message
    return json.dumps({'success': success, 'message': message})

if __name__ == '__main__':
    app.run()
