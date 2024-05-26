from flask import Flask, make_response, jsonify, request
from flask_mysqldb import MySQL
from flask_httpauth import HTTPBasicAuth
import dicttoxml

app = Flask(__name__)
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "root"
app.config["MYSQL_DB"] = "cars"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)
auth = HTTPBasicAuth()

# User data storage for demonstration
users = {
    "user1": "password1",
    "user2": "password2"
}

@auth.verify_password
def verify_password(username, password):
    if username in users and users[username] == password:
        return username
    return None

def convert_to_xml(data):
    xml = dicttoxml.dicttoxml(data, custom_root='response', attr_type=False)
    return xml

@app.route("/")
def hello_world():
    
    style = """
        <style>
            p {
                font-family: Arial, sans-serif;
                font-size: 50px;
                color: blue;
                text-align: center;
            }
        </style>
    """
    return f"{style} <p>WELCOME TO ACE DATABASE</p>"

@app.route("/cars", methods=["GET", "POST"])
@auth.login_required
def manage_cars():
    if request.method == "GET":
        cur = mysql.connection.cursor()
        query = "SELECT * FROM cars;"
        cur.execute(query)
        data = cur.fetchall()
        cur.close()

        response_format = request.args.get('format', 'json')
        if response_format == 'xml':
            response = make_response(convert_to_xml(data), 200)
            response.headers['Content-Type'] = 'application/xml'
        else:
            response = make_response(jsonify(data), 200)
            response.headers['Content-Type'] = 'application/json'
        return response
    elif request.method == "POST":
        car = request.json
        cur = mysql.connection.cursor()
        query = "INSERT INTO cars (model, year, color, manufacturer_id) VALUES (%s, %s, %s, %s);"
        cur.execute(
            query, (car["model"], car["year"], car["color"], car["manufacturer_id"])
        )
        mysql.connection.commit()
        cur.close()

        response_data = {"message": "Car added successfully"}
        response_format = request.args.get('format', 'json')
        if response_format == 'xml':
            response = make_response(convert_to_xml(response_data), 201)
            response.headers['Content-Type'] = 'application/xml'
        else:
            response = make_response(jsonify(response_data), 201)
            response.headers['Content-Type'] = 'application/json'
        return response

@app.route("/cars/<int:id>", methods=["GET", "PUT", "DELETE"])
@auth.login_required
def manage_car_by_id(id):
    if request.method == "GET":
        cur = mysql.connection.cursor()
        query = "SELECT * FROM cars WHERE car_id = %s;"
        cur.execute(query, (id,))
        data = cur.fetchone()
        cur.close()

        response_format = request.args.get('format', 'json')
        if data:
            if response_format == 'xml':
                response = make_response(convert_to_xml(data), 200)
                response.headers['Content-Type'] = 'application/xml'
            else:
                response = make_response(jsonify(data), 200)
                response.headers['Content-Type'] = 'application/json'
        else:
            error_data = {"message": "Car not found"}
            if response_format == 'xml':
                response = make_response(convert_to_xml(error_data), 404)
                response.headers['Content-Type'] = 'application/xml'
            else:
                response = make_response(jsonify(error_data), 404)
                response.headers['Content-Type'] = 'application/json'
        return response
    elif request.method == "PUT":
        car = request.json
        cur = mysql.connection.cursor()
        query = "UPDATE cars SET model = %s, year = %s, color = %s, manufacturer_id = %s WHERE car_id = %s;"
        cur.execute(
            query, (car["model"], car["year"], car["color"], car["manufacturer_id"], id)
        )
        mysql.connection.commit()
        cur.close()

        response_data = {"message": "Car updated successfully"}
        response_format = request.args.get('format', 'json')
        if response_format == 'xml':
            response = make_response(convert_to_xml(response_data), 200)
            response.headers['Content-Type'] = 'application/xml'
        else:
            response = make_response(jsonify(response_data), 200)
            response.headers['Content-Type'] = 'application/json'
        return response
    elif request.method == "DELETE":
        cur = mysql.connection.cursor()
        query = "DELETE FROM cars WHERE car_id = %s;"
        cur.execute(query, (id,))
        mysql.connection.commit()
        cur.close()

        response_data = {"message": "Car deleted successfully"}
        response_format = request.args.get('format', 'json')
        if response_format == 'xml':
            response = make_response(convert_to_xml(response_data), 200)
            response.headers['Content-Type'] = 'application/xml'
        else:
            response = make_response(jsonify(response_data), 200)
            response.headers['Content-Type'] = 'application/json'
        return response

if __name__ == "__main__":
    app.run(debug=True)
