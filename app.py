# Imports
from datetime import datetime

from flask import Flask, render_template, redirect, request
from flask_scss import Scss
import requests

auth = False
value_name = ["Last sync time", "Water Level", "Last Watered Time", "Soil Moisture", "Surrounding Temperature",
              "Humidity","Bird Count","Light"]
time_format = "%H:%M:%S %Y-%m-%d"
# My App Setup
app = Flask(__name__)
Scss(app)

#CHANGE TO pi IP and port
IP = "127.0.0.1:5050"

#path = "/home/DRevenant/GardeningSysBackend/"
path = ""


# Routes to Webpages
# Home page
@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        try:
            authentication = auth(request.form['key'])
            if authentication:
                values = [datetime.now().strftime(time_format),
                          request.form['WaterLevel'],
                          request.form['WaterLast'],
                          request.form['SoilMoist'],
                          request.form['SurroundTemp'],
                          request.form['Humidity'],
                          request.form['BirdCount'],
                          request.form['Light']]
                with open(path + "storage/values.txt", "w") as file:
                    file.write('\n'.join(values))
                print("Stored values")
            else:
                print("Authentication failed")
            return redirect("/")
        except Exception as e:
            print(f"ERROR:{e}")
            return f"ERROR:{e}"
    else:
        #if GET, then read values from file
        values = retrievevalues()
        print(values)
        return render_template('index.html', tasks=values, tasks_name=value_name)


@app.route("/data",methods=["GET"])
def getdata():
    return retrievevalues()

@app.route("/waterplant",methods=["GET"])
def waterplant():
    data = {
        'waterplant': '1',
        'motor': '0'
    }

    requests.post(IP, data=data)
    print("water!")

    return redirect("/")

@app.route("/activatemotor",methods=["GET"])
def activatemotor():
    data = {
        'waterplant': '0',
        'motor': '1'
    }

    requests.post(IP, data=data)
    print("motor!")

    return redirect("/")


def auth(key):
    with open(path + "storage/pwd.txt", "r") as file:
        contents = file.readlines()
        if key.strip() == contents[0].strip():
            return True
    return False


def retrievevalues():
    with open(path + "storage/values.txt", "r") as file:
        values = [line.strip() for line in file]
        return values


def convert(date_time):
    format = "%H:%M:%S %Y-%m-%d"
    datetime_str = datetime.strptime(date_time, time_format)

    return datetime_str


# Runner and Debugger
if __name__ == "__main__":
    app.run(debug=True)
