# Imports 
from flask import Flask, render_template, redirect, request
from flask_scss import Scss
from datetime import datetime
auth = False
values = []
value_name = ["Water Level", "Last Watered Time", "Soil Moisture", "Surrounding Temperature", "Humidity"]

# My App Setup
app = Flask(__name__)
Scss(app)

#path = "/home/DRevenant/GardeningSysBackend/"
path = ""

# Routes to Webpages
# Home page
@app.route("/",methods=["POST","GET"])
def index():
    # Add a Task
    if request.method == "POST":
        try:
            authentication = auth(request.form['key'])
            if authentication:
                print("Passed auth")
                values = []
                values.append(request.form['WaterLevel'])
                values.append(request.form['WaterLast'])
                values.append(request.form['SoilMoist'])
                values.append(request.form['SurroundTemp'])
                values.append(request.form['Humidity'])

                with open(path+"storage/values.txt","w") as file:
                    file.write('\n'.join(values))
                print("Stored values")
            else:
                print("Authentication failed")
            return redirect("/")
        except Exception as e:
            print(f"ERROR:{e}")
            return f"ERROR:{e}"
    # See all current tasks
    else:
        with open(path+"storage/values.txt", "r") as file:
            values = [line.strip() for line in file]
        print(values)
        return render_template('index.html', tasks=values, tasks_name=value_name)

def auth(key):
    with open(path+"storage/pwd.txt", "r") as file:
        contents = file.readlines()
        if key.strip() == contents[0].strip() :
            return True
    return False


# Runner and Debugger
if __name__ == "__main__":       
    app.run(debug=True)
    