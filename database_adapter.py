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
    c.execute("DROP TABLE IF EXISTS users")
    c.execute("CREATE TABLE users (user TEXT NOT NULL UNIQUE PRIMARY KEY, "
              "firstname TEXT NOT NULL, "
              "familyname TEXT NOT NULL, "
              "gender TEXT NOT NULL, "
              "city TEXT NOT NULL, "
              "country TEXT NOT NULL)"
              )
    c.execute("DROP TABLE IF EXISTS messages")
    c.execute("CREATE TABLE messages (id INTEGER PRIMARY KEY, "
              "user TEXT NOT NULL,"
              "writer TEXT NOT NULL,"
              "message TEXT NOT NULL)"
              )
    c.execute("DROP TABLE IF EXISTS passwords")
    c.execute("CREATE TABLE passwords (user TEXT NOT NULL UNIQUE PRIMARY KEY, "
              "password TEXT NOT NULL,"
              "salt TEXT NOT NULL)"
              )
    c.execute("DROP TABLE IF EXISTS loggedinusers")
    c.execute("CREATE TABLE loggedinusers (user TEXT NOT NULL UNIQUE PRIMARY KEY, "
              "token TEXT NOT NULL)"
              )
    c.commit()


def get_users():
    c = get_db()
    t = c.execute("SELECT username FROM users")
    return t.fetchone()