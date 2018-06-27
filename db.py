import sqlite3
import os
import json


def install(DATABASE):
    print "Installing..."
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute("PRAGMA foreign_keys = ON;")

    #Used for login
    cur.execute("CREATE TABLE login(id INTEGER PRIMARY KEY AUTOINCREMENT, username UNIQUE NOT NULL, password NOT NULL, admin BOOLEAN);")

    #Used for storing user data
    cur.execute("CREATE TABLE user(id INTEGER PRIMARY KEY AUTOINCREMENT, username UNIQUE NOT NULL, "
                "hours, personal, specialization,generated_classes, "
                "Challenge, Closeness, Curiosity, Excitement, Harmony,"
                "Ideal, Liberty, Love, Practicality, Selfexpression,"
                "Stability, Structure, Openness, Conscientiousness, Extraversion,"
                "Agreeableness, Emotionalrange, Conservation, Opennesstochange, Hedonism,"
                "Selfenhancement, Selftranscendence)")

    #Used to store Course Data
    cur.execute("CREATE TABLE classes(id INTEGER PRIMARY KEY AUTOINCREMENT, course NOT NULL, hours, rating, course_name,"
                "Challenge, Closeness, Curiosity, Excitement, Harmony,"
                "Ideal, Liberty, Love, Practicality, Selfexpression,"
                "Stability, Structure, Openness, Conscientiousness, Extraversion,"
                "Agreeableness, Emotionalrange, Conservation, Opennesstochange, Hedonism,"
                "Selfenhancement, Selftranscendence)")

    ##Test account
    cur.execute("INSERT INTO login (username, password, admin) VALUES ('123@123', '123123', 1)")
    cur.execute("INSERT INTO user(username,hours,personal) VALUES ('123@123', 100, 'Hello World I am awesome and how are you? Are you awesome? I am sad all the time?')")


    ##Add Course Data
    with open('ourcourses.json') as f:
        data = json.load(f)

    for i in data:
        course = str(i)
        hours = str(data[i]['workload'])
        rating = str(data[i]['rating'])
        course_name = str(data[i]['coursename'])
        cur.execute("INSERT INTO classes(course,hours,rating, course_name) "
                    "VALUES ('"+course+"','"+hours+"','"+rating+"','"+course_name+"')")

    ##Add Insights Data
    with open("insights.json") as f:
        idata = json.load(f)

    insights = {}
    for i in idata:
        temp = []
        for j in idata[i]:
            for k in j:
                temp.append(j[k])
        temp.append(i) #For where statement
        insights[i] = temp
        #print(temp)

    for i in insights:
        cur.execute("UPDATE classes "
                    "SET Challenge = ?,"
                    "Closeness = ?,"
                    "Curiosity = ?,"
                    "Excitement = ?,"
                    "Harmony = ?,"
                    "Ideal = ?,"
                    "Liberty = ?,"
                    "Love = ?,"
                    "Practicality = ?,"
                    "Selfexpression = ?,"
                    "Stability = ?,"
                    "Structure = ?,"
                    "Openness = ?,"
                    "Conscientiousness = ?,"
                    "Extraversion = ?,"
                    "Agreeableness = ?,"
                    "Emotionalrange = ?,"
                    "Conservation = ?,"
                    "Opennesstochange = ?,"
                    "Hedonism = ?,"
                    "Selfenhancement = ?,"
                    "Selftranscendence = ? WHERE course = ?", insights[i])


    insights['CS-6035'][len(insights['CS-6035'])-1] = "123@123"

    cur.execute("UPDATE user "
                "SET Challenge = ?,"
                "Closeness = ?,"
                "Curiosity = ?,"
                "Excitement = ?,"
                "Harmony = ?,"
                "Ideal = ?,"
                "Liberty = ?,"
                "Love = ?,"
                "Practicality = ?,"
                "Selfexpression = ?,"
                "Stability = ?,"
                "Structure = ?,"
                "Openness = ?,"
                "Conscientiousness = ?,"
                "Extraversion = ?,"
                "Agreeableness = ?,"
                "Emotionalrange = ?,"
                "Conservation = ?,"
                "Opennesstochange = ?,"
                "Hedonism = ?,"
                "Selfenhancement = ?,"
                "Selftranscendence = ? WHERE username = ?", insights['CS-6035'])


    conn.commit()
    #cur.execute("CREATE TABLE userInfo(id PRIMARY KEY, firstname, lastname);")

    # cur.execute("CREATE TABLE userClasses(id PRIMARY KEY, class_id, status)")
    # cur.execute("CREATE TABLE classes(id PRIMARY KEY, className, status);")
    # cur.execute("CREATE TABLE questions(id PRIMARY KEY, class, question, answer, comment)")
    # cur.execute("CREATE TABLE userAnswers(id PRIMARY KEY, userid, class, questionid, answer, points, timespent)")
    conn.close()
    return "Installed...OK!"


##############################
# database initialization
###############################
global DATABASE
DATABASE = 'freja.db'

if not os.path.exists(DATABASE):
    print(install(DATABASE))

if os.path.exists(DATABASE):
    print("Database exists...OK!")



