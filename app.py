# Imports 
from flask import Flask, render_template, redirect, request
from flask_scss import Scss
from datetime import datetime

# My App Setup
app = Flask(__name__)
Scss(app)

# Routes to Webpages
# Home page
@app.route("/",methods=["POST","GET"])
def index():
    # Add a Task
    if request.method == "POST":
        current_task = request.form['content']
        try:

            return redirect("/")
        except Exception as e:
            print(f"ERROR:{e}")
            return f"ERROR:{e}"
    # See all current tasks
    else:

        return render_template('index.html', tasks=tasks)

#https://www.home.com/delete
# Delete an Item
@app.route("/delete/<int:id>")
def delete(id:int):

    try:

        return redirect("/")
    except Exception as e:
        return f"ERROR:{e}"
    
    

# Edit an item
@app.route("/edit/<int:id>", methods=["GET","POST"])
def edit(id:int):

    if request.method == "POST":

        try:

            return redirect("/")
        except Exception as e:
            return f"Error:{e}"
    else:
        return render_template('edit.html',task=task)



def checkcredientials(username,password):
    with open("storage/pwd.txt","r") as file:
        contents = file.readlines()
        if username == contents[0] and password == contents[1]:
            return True
    return False


# Runner and Debugger
if __name__ == "__main__":       
    app.run(debug=True)
    