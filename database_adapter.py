import sqlite3

from flask import g


# connects to the local database
def connect_db():
    # type: () -> object
    conn = sqlite3.connect('C:\Users\skroo_000\Documents\Pear\database.db')
    return conn


# gets the database
def get_db():
    # type: () -> object
    db = getattr(g, 'db', None)
    if db is None:
        db = g.db = connect_db()

    return db


# creates all the tables, if not already created
def init():
    c = get_db()
    c.execute("DROP TABLE IF EXISTS storages")
    c.execute("CREATE TABLE storages (id INTEGER PRIMARY KEY, "
              "city TEXT NOT NULL)"
              )
    c.execute("DROP TABLE IF EXISTS products")
    c.execute("CREATE TABLE products (id INTEGER PRIMARY KEY, "
              "name TEXT NOT NULL, "
              "price INTEGER UNSIGNED NOT NULL)"
              )
    c.execute("DROP TABLE IF EXISTS io")
    c.execute("CREATE TABLE io (id INTEGER PRIMARY KEY, "
              "date DATE NOT NULL, "
              "product INTEGER NOT NULL, "
              "storage TEXT NOT NULL, "
              "amount TEXT NOT NULL) "
              # "FOREIGN KEY (product) REFERENCES products(id), "
              # "FOREIGN KEY (storage) REFERENCES storages(id))"
              )
    c.execute("DROP TABLE IF EXISTS stock")
    c.execute("CREATE TABLE stock (id INTEGER PRIMARY KEY, "
              "product INTEGER NOT NULL, "
              "storage TEXT NOT NULL, "
              "balance TEXT NOT NULL) "
              # "FOREIGN KEY (product) REFERENCES products(id), "
              # "FOREIGN KEY (storage) REFERENCES storages(id))"
              )
    c.commit()


# returns all storage city names
def get_storages():
    # type: () -> object
    c = get_db()
    u = c.execute("SELECT city FROM storages")
    result = u.fetchall()
    storages = []
    for row in result:
        data = row[0]
        storages.append(data)
    return storages


# returns city name of the storage with called id
def get_storage_by_id(storage_id):
    # type: (int) -> str
    c = get_db()

    u = c.execute("SELECT city FROM storages WHERE id = ?", (storage_id,))
    return ''.join(u.fetchone())


# returns the name of the product with called id
def get_product_by_id(product_id):
    # type: (int) -> str
    c = get_db()

    u = c.execute("SELECT name FROM products WHERE id = ?", (product_id,))
    return ''.join(u.fetchone())


# returns the stock(s) with called storage name
def get_stock_by_storage_name(storage_name):
    # type: (str) -> object
    c = get_db()

    u = c.execute("SELECT * FROM stock WHERE storage = ?", (storage_name,))
    result = u.fetchall()
    list_of_data = []
    for row in result:
        data = {"product": row[1], "storage": row[2], "balance": row[3]}
        list_of_data.append(data)
    return list_of_data


# returns the io(s) with called storage name
def get_io_by_storage_name(storage_name):
    # type: (str) -> object
    c = get_db()

    u = c.execute("SELECT * FROM io WHERE storage = ?", (storage_name,))
    result = u.fetchall()
    list_of_data = []
    for row in result:
        data = {"date": row[1], "product": row[2], "storage": row[3], "amount": row[4]}
        list_of_data.append(data)
    return list_of_data


# check if product exists
def product_exists(product_name):
    # type: (str) -> bool
    c = get_db()

    u = c.execute("SELECT name FROM products WHERE name = ?", (product_name,))
    return u.fetchone() is not None


# check if storage exists
def storage_exists(storage_name):
    # type: (str) -> bool
    c = get_db()
    u = c.execute("SELECT city FROM storages WHERE city = ?", (storage_name,))
    return u.fetchone() is not None


# adds io shipment
def add_io(ship_date, product_name, storage_name, ship_amount):
    # type: (Date, string, string, int) -> bool
    c = get_db()
    if product_exists(product_name) and storage_exists(storage_name):
        c.execute("INSERT INTO io (date, product, storage, amount) VALUES (?,?,?,?)",
                  (ship_date, product_name, storage_name, ship_amount))
        c.commit()
        return True
    else:
        return False


# updates stock balance
def update_stock(product_name, storage_name, add_to_balance):
    # type: (string, string, int) -> bool
    c = get_db()
    if product_exists(product_name) and storage_exists(storage_name):
        u = c.execute("SELECT * FROM stock WHERE product = ? AND storage = ?", (product_name, storage_name))
        result = u.fetchone()
        new_balance = int(result[3]) + int(add_to_balance)
        c.execute("DELETE FROM stock WHERE product = ? AND storage = ?", (product_name, storage_name))
        c.execute("INSERT INTO stock (product, storage, balance) VALUES (?,?,?)",
                  (product_name, storage_name, new_balance))
        c.commit()
        return True
    else:
        return False
