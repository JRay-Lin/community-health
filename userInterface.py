# -*- coding: UTF-8 -*-

from flask import Flask, render_template, request


# create Flask app
app = Flask(__name__)
app._static_folder = "./templates/static"


# main page
@app.route("/")
def home():
    return render_template("index.html")


# new user page
@app.route("/newUser")
def new_user():
    return render_template("newUser.html")


@app.route("/data", methods=["POST"])
def data():
    user_data = request.form["data"]
    return f"你提交的數據是: {user_data}"


if __name__ == "__main__":
    app.run(debug=True)
