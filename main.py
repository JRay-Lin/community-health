import sqlite3
import userInterface


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


def historyData(user):  # get history data from database
    pass


def newHealthData(user):  # modify health data
    pass


def modifyHealthData(user):  # modify health data
    pass


def userData():  # modify user data
    pass


if __name__ == "__main__":
    tableChecker()
    userInterface.app.run(debug=True)
