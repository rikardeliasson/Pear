import sqlite3
import string

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
              "product TEXT NOT NULL, "
              "storage TEXT NOT NULL, "
              "amount INTEGER NOT NULL, "
              "FOREIGN KEY (product) REFERENCES products(id), "
              "FOREIGN KEY (storage) REFERENCES storages(id))"
              )
    c.execute("DROP TABLE IF EXISTS stock")
    c.execute("CREATE TABLE stock (id INTEGER PRIMARY KEY, "
              "product TEXT NOT NULL, "
              "storage TEXT NOT NULL, "
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
