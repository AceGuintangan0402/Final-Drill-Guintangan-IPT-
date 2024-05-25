from flask import Flask, make_response, jsonify, request
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "root"
app.config["MYSQL_DB"] = "classicmodels"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)

@app.route("/")  # Add the @ symbol here
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/customers", methods=["GET"])  # Add the @ symbol here
def get_customers():
    cur = mysql.connection.cursor()
    query = "SELECT * FROM classicmodels.customers;"
    cur.execute(query)
    data = cur.fetchall()
    cur.close()
    return make_response(jsonify(data), 200)

if __name__ == "__main__":
    app.run(debug=True)
