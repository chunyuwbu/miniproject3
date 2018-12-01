import argparse
import sys
from google.cloud import videointelligence
import io
import mysql.connector
import pymongo
import os


def analyze(path, username, img_num):
    # here should be your own json file at current directory

    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getcwd() + '/google.json'

    video_client = videointelligence.VideoIntelligenceServiceClient()
    features = [videointelligence.enums.Feature.LABEL_DETECTION]
    with io.open(path, 'rb') as movie:
        input_content = movie.read()
    try:
        operation = video_client.annotate_video(features=features, input_content=input_content)
        print('\nProcessing video:')
        result = operation.result(timeout=90)
    except Exception as e:
        print("Video Intelligence error")
        print(e)
        exit()

    print('\nFinished processing.')

    # Process video/segment level label annotations
    desc = ""
    c = 0
    segment_labels = result.annotation_results[0].segment_label_annotations
    for i, segment_label in enumerate(segment_labels):
        print(('Video label description: {}'.format(segment_label.entity.description)))
        desc = desc + segment_label.entity.description + ","
        c = c + 1
        for category_entity in segment_label.category_entities:
            print("Label category description: " + category_entity.description, )

        for i, segment in enumerate(segment_label.segments):
            confidence = segment.confidence
            print("The accuracy of the identification in this case is " + str(confidence) + "\n")

    # insert to mysql db
    mydb = mysql.connector.connect(host="localhost", user="root", passwd="123456",
                                   auth_plugin='mysql_native_password')
    mycursor = mydb.cursor()
    mycursor.execute("use mini_project3_db")
    sql = "INSERT INTO user_data (username, img_num,description,description_num) VALUES (%s, %s,%s,%s)"
    desc = desc[:-1]
    val = (username, img_num, desc, c)
    mycursor.execute(sql, val)

    mydb.commit()

    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["mydatabase"]
    mycol = mydb["users"]
    mydict = {"username": username, "img_num": img_num, "description": desc, "description_num": c}
    x = mycol.insert_one(mydict)