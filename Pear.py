from flask import Flask
from flask import render_template

import database_adapter as db
import json

app = Flask(__name__)


@app.route('/')
def root():
    return render_template("client.html")


@app.route('/init_db')
def init_db():
    db.init()
    return "Database Initialized"


@app.route('/print')
def print_storages():
    storages = db.get_storages()
    if storages is not None:
        return create_response_data(True, "Storages retrieved", storages)
    else:
        return create_response(False, "Failed to retrieve storages")


@app.route("/get_storage_by_id/<storage_id>")
def get_storage_by_id(storage_id):
    data = db.get_storage_by_id(storage_id)
    if data is not None:
        return create_response_data(True, "Storage_retrieved", data)
    else:
        return create_response(False, "No such storage")


@app.route("/get_product_by_id/<product_id>")
def get_product_by_id(product_id):
    data = db.get_product_by_id(product_id)
    if data is not None:
        return create_response_data(True, "Product_retrieved", data)
    else:
        return create_response(False, "No such product")


@app.route("/add_io/<ship_date>/<product_name>/<storage_name>/<ship_amount>")
def add_io(ship_date, product_name, storage_name, ship_amount):
    if db.add_io(ship_date, product_name, storage_name, ship_amount):
        return create_response(True, "io created")
    else:
        return create_response(False, "Failed to create io")


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
