from flask import Flask
from flask import render_template

import database_adapter as db

app = Flask(__name__)


@app.route('/')
def root():
    return render_template("client.html")


@app.route('/init_db')
def init_db():
    db.init()
    return "Database Initialized"


@app.route('/print')
def print_users():
    return db.get_users()


if __name__ == '__main__':
    app.run()
