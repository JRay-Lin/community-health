import os
import sqlite3
import pandas as pd
from flask import flash
import matplotlib
from matplotlib import pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg
from datetime import datetime


# remove old picture
def removeOldPicture():
    if os.path.exists("templates/static/picture/bp.png"):
        os.remove("templates/static/picture/bp.png")

    if os.path.exists("templates/static/picture/bs.png"):
        os.remove("templates/static/picture/bs.png")

    if os.path.exists("templates/static/picture/weight.png"):
        os.remove("templates/static/picture/weight.png")


# check if table needed is not exist
def tableChecker():
    # connect to database
    database = sqlite3.connect("database.db")
    cursor = database.cursor()

    # create user table if not exist
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS user (id INTEGER PRIMARY KEY, name TEXT, birthday TEXT, gender TEXT, height INTEGER)"
    )

    # create health data table if not exist
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS data (id INTEGER PRIMARY KEY, user_id INTEGER, date TEXT, weight INTEGER, bpc INTEGER, bpr INTEGER,bs INTEGER)"
    )

    # exit database
    database.close()


# add new user to database
def addUser(name, birthday, gender, height):  # add new user to database
    # connect to database
    database = sqlite3.connect("database.db")
    cursor = database.cursor()

    try:
        # add user to database
        cursor.execute(
            "INSERT INTO user (name, birthday, gender, height) VALUES (?, ?, ?, ?)",
            (name, birthday, gender, height),
        )

        database.commit()
        flash("使用者資料已上傳", "success")
    except Exception as e:
        flash("Error: add user failed", "error")
    finally:
        database.close()


# get user list from database
def userList():
    # connect to database
    database = sqlite3.connect("database.db")
    cursor = database.cursor()

    cursor.execute("SELECT * FROM user")
    users = cursor.fetchall()
    database.close()
    return users


# delete user from database
def delUser(name_id):
    # connect to database
    database = sqlite3.connect("database.db")
    cursor = database.cursor()

    cursor.execute("DELETE FROM user WHERE id=?", (name_id,))
    database.commit()
    database.close()
    flash("使用者資料已刪除", "success")


# add new health data to database
def addHealthData(user_id, date, weight, bpc, bpr, bs):
    # connect to database
    database = sqlite3.connect("database.db")
    cursor = database.cursor()

    try:
        # add health data to database
        cursor.execute(
            "INSERT INTO data (user_id, date, weight, bpc, bpr, bs) VALUES (?, ?, ?, ?, ?, ?)",
            (user_id, date, weight, bpc, bpr, bs),
        )

        database.commit()
        flash("健康資料已上傳", "success")
    except Exception as e:
        flash("Error: add data failed", "error")
    finally:
        database.close()


# search health history and plot
def healthHistory(user_id):
    # connect to database
    database = sqlite3.connect("database.db")
    cursor = database.cursor()

    # get data from database
    cursor.execute(
        "SELECT date, weight, bpc, bpr, bs FROM data WHERE user_id=?", (user_id,)
    )
    datas = cursor.fetchall()
    database.close()

    # turn datas to pandas dataframe
    df = pd.DataFrame(datas, columns=["date", "weight", "bpc", "bpr", "bs"])
    df["date"] = pd.to_datetime(df["date"])  # convert to datetime
    df["date"] = df["date"].dt.strftime("%m-%d")

    # create figures and axes for plotting
    matplotlib.use("agg")
    fig1, ax1 = plt.subplots(figsize=(6, 4))  # set the figure width to 800px
    fig2, ax2 = plt.subplots(figsize=(6, 4))  # set the figure width to 800px
    fig3, ax3 = plt.subplots(figsize=(6, 4))  # set the figure width to 800px

    # Plot Weight Over Time
    ax1.plot(df["date"], df["weight"])
    ax1.set_xlabel("Date")
    ax1.set_ylabel("Weight (kg)")
    ax1.tick_params(axis="x", rotation=45)
    fig1.tight_layout()  # adjust layout
    fig1.savefig("templates/static/picture/weight.png")

    # Plot Blood Pressure Over Time
    ax2.plot(df["date"], df["bpc"], color="b", label="Systolic")
    ax2.set_xlabel("Date")
    ax2.set_ylabel("Systolic Blood Pressure", color="b")
    ax2.tick_params(axis="x", rotation=45)
    ax2.tick_params(axis="y", labelcolor="b")

    ax4 = ax2.twinx()
    ax4.plot(df["date"], df["bpr"], color="r", label="Diastolic")
    ax4.set_ylabel("Diastolic Blood Pressure", color="r")
    ax4.tick_params(axis="y", labelcolor="r")

    fig2.tight_layout()  # adjust layout
    fig2.savefig("templates/static/picture/bp.png")

    # Plot Blood Sugar Over Time
    ax3.plot(df["date"], df["bs"])
    ax3.set_xlabel("Date")
    ax3.set_ylabel("Blood Sugar (mg/dL)")
    ax3.tick_params(axis="x", rotation=45)
    fig3.tight_layout()  # adjust layout
    fig3.savefig("templates/static/picture/bs.png")

    # clear the plots after saving to avoid overlapping of plots in future calls
    plt.clf()
