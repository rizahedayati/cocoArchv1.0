import mysql.connector
import json
from flask import Flask
from flask import request, jsonify
from typing import Optional
import redis
from config import BaseConfig
import json
# app = Flask(__name__)
# cache = redis.Redis(host='redis', port=6379)

from flask_caching import Cache


app = Flask(__name__)
app.config.from_object(BaseConfig)
cache = Cache(app)


@app.route('/')
def hello_world():
    return "hello world"


@app.route('/square/<int:number>')
@cache.cached(timeout=30, query_string=True)
def square(number):
    app.logger.info(f"Computing the square of {number}")
    return jsonify({"computed": number*number})


@app.route('/widgets')
def get_widgets():
    mydb = mysql.connector.connect(
        host="db",
        user="root",
        password="p@ssw0rd1",
        database="inventory"
    )
    cursor = mydb.cursor()

    cursor.execute("SELECT * FROM widgets")

    # this will extract row headers
    row_headers = [x[0] for x in cursor.description]

    results = cursor.fetchall()
    json_data = []
    for result in results:
        json_data.append(dict(zip(row_headers, result)))

    cursor.close()

    return json.dumps(json_data)


@app.route('/initdb')
def db_init():
    mydb = mysql.connector.connect(
        host="db",
        user="root",
        password="p@ssw0rd1"
    )
    cursor = mydb.cursor()

    cursor.execute("DROP DATABASE IF EXISTS inventory")
    cursor.execute("CREATE DATABASE inventory")
    cursor.close()

    mydb = mysql.connector.connect(
        host="db",
        user="root",
        password="p@ssw0rd1",
        database="inventory"
    )
    cursor = mydb.cursor()

    cursor.execute("DROP TABLE IF EXISTS widgets")
    cursor.execute(
        "CREATE TABLE widgets (name VARCHAR(255), description VARCHAR(255))")
    cursor.close()

    return 'init database'


if __name__ == "__main__":
    app.run(host='0.0.0.0')
