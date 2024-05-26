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
        query = "INSERT INTO cars (model, year, color, manufacturer_id) VALUES (%s, %s, %s, %s);"
        cur.execute(
            query, (car["model"], car["year"], car["color"], car["manufacturer_id"])
        )
        mysql.connection.commit()
        cur.close()
        return make_response(jsonify({"message": "Car added successfully"}), 201)


@app.route("/cars/<int:id>", methods=["GET", "PUT","DELETE"])
def manage_car_by_id(id):
    if request.method == "GET":
        cur = mysql.connection.cursor()
        query = "SELECT * FROM cars WHERE car_id = %s;"
        cur.execute(query, (id,))
        data = cur.fetchone()
        cur.close()
        if data:
            return make_response(jsonify(data), 200)
        else:
            return make_response(jsonify({"message": "Car not found"}), 404)
    elif request.method == "PUT":
        car = request.json
        cur = mysql.connection.cursor()
        query = "UPDATE cars SET model = %s, year = %s, color = %s, manufacturer_id = %s WHERE car_id = %s;"
        cur.execute(
            query, (car["model"], car["year"], car["color"], car["manufacturer_id"], id)
        )
        mysql.connection.commit()
        cur.close()
        return make_response(jsonify({"message": "Car updated successfully"}), 200)
    
    elif request.method == "DELETE":
        cur = mysql.connection.cursor()
        query = "DELETE FROM cars WHERE car_id = %s;"
        cur.execute(query, (id,))
        mysql.connection.commit()
        cur.close()
        return make_response(jsonify({"message": "Car deleted successfully"}), 200)


if __name__ == "__main__":
    app.run(debug=True)
