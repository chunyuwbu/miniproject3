
import sys
import get_images as get_images
import convert_to_video as create_video
import google_analysis as analyze_video
import mysql_db as mysql_func
import mongo_db as mongo_func
import pymongo
import mysql.connector
from statistics import mode


def get_input_num():
    num = None
    while num is None:
        try:
            num = int(input("Enter a number: "))
        except ValueError:
            print("Program halted incorrect data entered,please Enter a number ")
    return num


MYSQL = 1


def main():
    while (1):
        mydb = mysql.connector.connect(host="localhost", user="root", passwd="123456",
                                       auth_plugin='mysql_native_password')
        mycursor = mydb.cursor()
        mycursor.execute("CREATE DATABASE IF NOT EXISTS  mini_project3_db")
        mycursor.execute("use mini_project3_db")
        mycursor.execute(
            "CREATE TABLE  IF NOT EXISTS user_data (id INT AUTO_INCREMENT PRIMARY KEY,username VARCHAR(255), img_num VARCHAR(255),description VARCHAR(255),description_num VARCHAR(255))")
        mycursor.execute("use mini_project3_db")
        print("------------------------------------------------")
        print(
            "Menu:\n1.Query new user name\n2.Query exist user name\n3.See full database \n4.Delete DataBase\n5.Search for a word\n6.Exit")
        data = get_input_num();

        if (data == 1):
            # add always to both db,add is at analyze_video
            mysql_func.add_user(mycursor)
        elif (data == 2):
            print("Insert a Data Base to query:\n1.MySQL\n2.MongoDB")
            db = get_input_num()
            if (db == MYSQL):
                mysql_func.query_user(mycursor)
            else:
                mongo_func.query_user()

        elif (data == 3):
            print("Insert a Data Base to query:\n1.MySQL\n2.MongoDB")
            db = get_input_num()
            if (db == MYSQL):
                mysql_func.print_db(mycursor)
            else:
                mongo_func.print_db()
        elif (data == 4):
            # delete always both sb
            mysql_func.delete_db(mycursor)
            mongo_func.delete_db()
        elif (data == 5):
            print("Insert a Data Base to query:\n1.MySQL\n2.MongoDB")
            db = get_input_num()
            if (db == MYSQL):
                mysql_func.search_word(mycursor)
            else:
                mongo_func.search_word()

        elif (data == 6):
            return


main()