from flask import Flask,render_template,jsonify,request
from flask_mysqldb import MySQL
import config
import pickle
import json
import numpy as np

app = Flask(__name__)

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "Shilpa291994"
app.config["MYSQL_DB"] = "db_iris"
mysql = MySQL(app)


with open(config.JSON_DATA_PATH,"r") as f:
    data_json = json.load(f)

with open(config.MODEL_PATH,"rb") as f:
    model = pickle.load(f)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/Class",methods = ["GET","POST"])
def pred():
    data = request.form
    test_array = np.zeros(4)
    test_array[0] = eval(data["sepallength"])
    a = test_array[0]
    test_array[1] = eval(data["sepalwidth"])
    b = test_array[1]
    test_array[2] = eval(data["petallength"])
    c = test_array[2]
    test_array[3] = eval(data["petalwidth"])
    d = test_array[3]
    result = model.predict([test_array])[0]

    cursor = mysql.connection.cursor()
    query = 'CREATE TABLE IF NOT EXISTS Iris_flower(SEPALLENGTH VARCHAR(20),SEPALWIDTH VARCHAR(20),PETALLENGTH VARCHAR(20),PETALWIDTH VARCHAR(20),CLASS VARCHAR(20))'
    cursor.execute(query)
    cursor.execute('INSERT INTO Iris_flower(SEPALLENGTH,SEPALWIDTH,PETALLENGTH,PETALWIDTH,CLASS) VALUES (%s,%s,%s,%s,%s)',(a,b,c,d,result))

    mysql.connection.commit()
    cursor.close()    

    return render_template("index1.html",result = result)

if __name__ == "__main__":
    app.run(host = "0.0.0.0",port = config.PORT_NUMBER )    