from flask import Flask, make_response, jsonify, request
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

@app.route("/cars", methods=["GET", "POST"])
def manage_cars():
    if request.method == "GET":
        cur = mysql.connection.cursor()
        query = "SELECT * FROM cars;"
        cur.execute(query)
        data = cur.fetchall()
        cur.close()
        return make_response(jsonify(data), 200)
    elif request.method == "POST":
        car = request.json
        cur = mysql.connection.cursor()
        query = "INSERT INTO cars (manufacturer_id, model, year, color) VALUES (%s, %s, %s, %s);"
        cur.execute(query, (car['manufacturer_id'], car['model'], car['year'], car['color']))
        mysql.connection.commit()
        cur.close()
        return make_response(jsonify({"message": "Car added successfully"}), 201)

@app.route("/cars/<int:id>", methods=["GET"])
def get_cars_by_id(id):
    cur = mysql.connection.cursor()
    query = "SELECT * FROM cars WHERE car_id = %s;"
    cur.execute(query, (id,))
    data = cur.fetchone()  # Fetch one result for the given ID
    cur.close()
    if data:
        return make_response(jsonify(data), 200)
    else:
        return make_response(jsonify({"message": "Car not found"}), 404)

if __name__ == "__main__":
    app.run(debug=True)
