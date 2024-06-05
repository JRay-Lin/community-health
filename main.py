# -*- coding: UTF-8 -*-


import sqlite3
from flask import Flask, request, flash, redirect, url_for, render_template
from datetime import datetime


def tableChecker():  # check if table not exist
    # connect to database
    databse = sqlite3.connect("database.db")
    cursor = databse.cursor()

    # create user table if not exist
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS user (id INTEGER PRIMARY KEY, name TEXT, birthday TEXT, gender TEXT, height INTERGER)"
    )

    # create health data table if not exist
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS data (id INTEGER PRIMARY KEY, user_id INTEGER, date TEXT, weight INTERGER, bp INTERGER, bs INTERGER)"
    )

    # exit database
    databse.close


def addUser(name, birthday, gender, height):  # add new user to database
    database = sqlite3.connect("database.db")
    cursor = database.cursor()

    try:
        # add user to database
        cursor.execute(
            "INSERT INTO user (name, birthday, gender, height) VALUES (?, ?, ?, ?)",
            (name, birthday, gender, height),
        )

        database.commit()
        database.close()
        print("Add user success")
    except:
        print("Error: add user failed")


def userList():  # get user list from database
    database = sqlite3.connect("database.db")
    cursor = database.cursor()
    cursor.execute("SELECT * FROM user")
    users = cursor.fetchall()
    database.close()
    return users


def modifyUser():  # modify user data
    pass


def historyData(user):  # get history data from database
    pass


def newHealthData(user):  # modify health data
    pass


def modifyHealthData(user):  # modify health data
    pass


# create Flask app
app = Flask(__name__)
app._static_folder = "./templates/static"
app.secret_key = "your_secret_key"


# main page
@app.route("/")
def index():
    users = userList()
    print(users)
    return render_template("index.html", users=users)


# new user
@app.route("/newuser", methods=["GET", "POST"])
def new_user():
    if request.method == "POST":
        name = request.form.get("name")
        birthday = request.form.get("birthday")
        gender = request.form.get("gender")
        height = request.form.get("height")

        # 檢查日期格式
        if not birthday:
            flash("請輸入有效的日期格式 (yyyy-mm-dd)", "error")
            return redirect(url_for("new_user"))

        try:
            birthday_date = datetime.strptime(birthday, "%Y-%m-%d").date()
        except ValueError:
            flash("請輸入有效的日期格式 (yyyy-mm-dd)", "error")
            return redirect(url_for("new_user"))

        if birthday_date > datetime.today().date():
            flash("日期不能超過今天", "error")
            return redirect(url_for("new_user"))

        try:
            height = float(height)  # type: ignore
            if height < 70 or height > 270:
                flash("請輸入有效的身高", "error")
                return redirect(url_for("new_user"))
        except ValueError:
            flash("身高僅能輸入數字", "error")
            return redirect(url_for("new_user"))

        addUser(name, birthday_date, gender, height)  # 確保存儲浮點數
        flash("使用者資料已上傳", "success")
        return redirect(url_for("new_user"))

    return render_template("index.html")


if __name__ == "__main__":
    tableChecker()
    app.run(debug=True)
