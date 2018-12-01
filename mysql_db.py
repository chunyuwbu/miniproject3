import get_images as get_images
import convert_to_video as create_video
import google_analysis as analyze_video

def query_user(mycursor):
    screen_name =input("Enter a user name to query: ")
    mycursor.execute("SELECT * FROM user_data WHERE username='"+screen_name+"'")
    myresult = mycursor.fetchall()
    if (len(myresult)==0):
        print("No such user name")
    else:
        for user in myresult:
            print(user)

def print_db(mycursor):
    mycursor.execute(("SELECT * FROM user_data"))
    myresult = mycursor.fetchall()
    print("There are ",len(myresult),"users at data base")
    print("The current data base is ")
    avg_im=0
    desc=[]
    for user in myresult:
        avg_im=avg_im+int(user[2])
        curr_des=user[3].split(',')
        for j in curr_des:
            desc.append(j)
        print(user)
    if (len(myresult)>0):
        print("Some statistics:")
        print("The most popular description is",(max(set(desc), key = desc.count)))
        print("There is an average of",str(avg_im/len(myresult)),"images per feed")
    return

def delete_db(mycursor):
    mycursor.execute("truncate user_data;")
    return

def search_word(mycursor):
    word=input("Enter a word to search: ")
    mycursor.execute(("SELECT * FROM user_data"))
    myresult = mycursor.fetchall()
    print("The next user has the word",word,"in their description:")
    for user in myresult:
        desc=user[3]
        desc=desc.split(',')
        if word in desc:
            print(user[1])

def add_user(mycursor):
    screen_name =input("Enter a user name: ")
    mycursor.execute("SELECT * FROM user_data WHERE username='"+screen_name+"'")
    myresult = mycursor.fetchall()
    if (len(myresult)!=0):
        print("User name already exist")
        return
    print(screen_name)
    print("-------------------------------------")
    print("downloading images from tweeter feed " + screen_name)
    print("-------------------------------------")
    img_num=get_images.get_images_from_user(screen_name)
    print("-------------------------------------")
    print("creating video from ",str(img_num)," images")
    print("-------------------------------------")
    create_video.create(screen_name)
    print("-------------------------------------")
    print("analyzing video")
    print("-------------------------------------")
    analyze_video.analyze(screen_name+".mp4",screen_name,img_num)
    return