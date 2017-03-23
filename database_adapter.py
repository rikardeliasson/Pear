import sqlite3

from flask import g


# connects to the local database
def connect_db():
    # type: () -> object
    conn = sqlite3.connect('C:\Users\skroo_000\Documents\Pear\database.db')
    return conn


# get the database
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
              "storage INTEGER NOT NULL, "
              "amount INTEGER NOT NULL, "
              "FOREIGN KEY (product) REFERENCES products(id), "
              "FOREIGN KEY (storage) REFERENCES storages(id))"
              )
    c.execute("DROP TABLE IF EXISTS stock")
    c.execute("CREATE TABLE stock (id INTEGER PRIMARY KEY, "
              "product INTEGER NOT NULL, "
              "storage INTEGER NOT NULL, "
              "balance INTEGER NOT NULL, "
              "FOREIGN KEY (product) REFERENCES products(id), "
              "FOREIGN KEY (storage) REFERENCES storages(id))"
              )
    c.commit()


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


def get_storage_by_id(storage_id):
    # type: (int) -> str
    c = get_db()

    u = c.execute("SELECT city FROM storages WHERE id = ?", (storage_id,))
    return ''.join(u.fetchone())


def get_product_by_id(product_id):
    # type: (int) -> str
    c = get_db()

    u = c.execute("SELECT name FROM products WHERE id = ?", (product_id,))
    return ''.join(u.fetchone())


# TODO: add help functions product_exists(product_name) amd storage_exists(storage_name)
def add_io(ship_date, product_id, storage_id, ship_amount):
    #type: (Date, int, int, int) -> bool
    c = get_db()

    c.execute("INSERT INTO io (date, product, storage, amount) VALUES (?,?,?,?)",
              (ship_date, product_id, storage_id, ship_amount))
    c.commit()
    return True
