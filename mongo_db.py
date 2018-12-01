import get_images as get_images
import convert_to_video as create_video
import google_analysis as analyze_video
import pymongo


def query_user():
    screen_name = input("Enter a user name to query: ")
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["mydatabase"]
    mycol = mydb["users"]

    if (mycol.count() == 0):
        print("No such user name")
    else:
        for user in mycol.find():
            if (user.get('username') == screen_name):
                print(user)


def print_db():
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["mydatabase"]
    mycol = mydb["users"]
    print("There are ", mycol.count(), "users at data base")
    print("The current data base is :")
    avg_im = 0
    desc = []
    for user in mycol.find():
        print(user)
        avg_im = avg_im + user.get('img_num')
        curr_des = user.get('description').split(',')
        for j in curr_des:
            desc.append(j)
    if (mycol.count() > 0):
        print("Some statistics:")
        print("The most popular description is", (max(set(desc), key=desc.count)))
        print("There is an average of", str(avg_im / mycol.count()), "images per feed")
    return


def delete_db():
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["mydatabase"]
    mycol = mydb["users"]
    x = mycol.delete_many({})
    return


def search_word():
    word = input("Enter a word to search: ")
    print("The next user has the word", word, "in their description:")
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["mydatabase"]
    mycol = mydb["users"]
    for user in mycol.find():
        desc = user.get('description')
        desc = desc.split(',')
        if word in desc:
            print(user.get('username'))
