from flask import Flask, make_response, jsonify
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "root"
app.config["MYSQL_DB"] = "cars"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)

@app.route("/")  
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/cars", methods=["GET"])  
def get_cars():
    cur = mysql.connection.cursor()
    query = "SELECT * FROM cars;"
    cur.execute(query)
    data = cur.fetchall()
    cur.close()
    return make_response(jsonify(data), 200)

@app.route("/cars/<int:id>", methods=["GET"])
def get_cars_by_manufacturer(id):
    cur = mysql.connection.cursor()
    query = "SELECT * FROM cars WHERE car_id = %s;"
    cur.execute(query, (id,))
    data = cur.fetchall()  # Fetch all results for the given ID
    cur.close()
    return make_response(jsonify(data), 200)

if __name__ == "__main__":
    app.run(debug=True)
