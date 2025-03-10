# Imports 
from flask import Flask, render_template, redirect, request
from flask_scss import Scss
from datetime import datetime
auth = False
values = []
# My App Setup
app = Flask(__name__)
Scss(app)

# Routes to Webpages
# Home page
@app.route("/",methods=["POST","GET"])
def index():
    # Add a Task
    if request.method == "POST":
        try:
            authentication = auth(request.form['key'])
            if authentication:
                values = []
                values.append(request.form['WaterLevel'])
                values.append(request.form['WaterLast'])
                values.append(request.form['SoilMoist'])
                values.append(request.form['SurroundTemp'])
                values.append(request.form['Humidity'])

                with open("storage/values.txt","w") as file:
                    file.write(values)
                print("Stored values")
            else:
                print("Authentication failed")
            return redirect("/")
        except Exception as e:
            print(f"ERROR:{e}")
            return f"ERROR:{e}"
    # See all current tasks
    else:
        with open("storage/values.txt", "r") as file:
            values = [line.strip() for line in file]
        return render_template('index.html', tasks=values)

def auth(key):
    with open("storage/pwd.txt", "r") as file:
        contents = file.readlines()
        if key == contents:
            return True
    return False


# Runner and Debugger
if __name__ == "__main__":       
    app.run(debug=True)
    