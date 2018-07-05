from flask import Blueprint, render_template, session,abort
from db import *
import random
import json

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def quick_value(mypersonalities,course):
    conn2 = sqlite3.connect(DATABASE)
    conn2.row_factory = dict_factory
    cur2 = conn2.cursor()
    cur2.execute("SELECT * FROM classes WHERE course = '"+course+"'")
    i = cur2.fetchone()
    delta1 = abs(float(i['Challenge']) - float(mypersonalities[0]))
    delta2 = abs(float(i['Closeness']) - float(mypersonalities[1]))
    delta3 = abs(float(i['Curiosity']) - float(mypersonalities[2]))
    delta4 = abs(float(i['Excitement']) - float(mypersonalities[3]))
    delta5 = abs(float(i['Harmony']) - float(mypersonalities[4]))
    delta6 = abs(float(i['Ideal']) - float(mypersonalities[5]))
    delta7 = abs(float(i['Liberty']) - float(mypersonalities[6]))
    delta8 = abs(float(i['Love']) - float(mypersonalities[7]))
    delta9 = abs(float(i['Practicality']) - float(mypersonalities[8]))
    delta10 = abs(float(i['Selfexpression']) - float(mypersonalities[9]))
    delta11 = abs(float(i['Stability']) - float(mypersonalities[10]))
    delta12 = abs(float(i['Structure']) - float(mypersonalities[11]))
    delta13 = abs(float(i['Openness']) - float(mypersonalities[12]))
    delta14 = abs(float(i['Conscientiousness']) - float(mypersonalities[13]))
    delta15 = abs(float(i['Extraversion']) - float(mypersonalities[14]))
    delta16 = abs(float(i['Agreeableness']) - float(mypersonalities[15]))
    delta17 = abs(float(i['Emotionalrange']) - float(mypersonalities[16]))
    delta18 = abs(float(i['Conservation']) - float(mypersonalities[17]))
    delta19 = abs(float(i['Opennesstochange']) - float(mypersonalities[18]))
    delta20 = abs(float(i['Hedonism']) - float(mypersonalities[19]))
    delta21 = abs(float(i['Selfenhancement']) - float(mypersonalities[20]))
    delta22 = abs(float(i['Selftranscendence']) - float(mypersonalities[21]))
    sumdelta = (delta1 + delta2 + delta3 + delta4 + delta5 + delta6 + delta7 + delta8 + delta9 + delta10 + delta11 + \
              delta12 + delta13 + delta14 + delta15 + delta16 + delta17 + delta18 + delta19 + delta20 + delta21 + delta22)/22
    conn2.close()
    return sumdelta

app_index = Blueprint('app_index',__name__)
@app_index.route("/")
@app_index.route("/index")
def index():
    authors = ["Andrey Makhanov", "Ryan Lewis"]
    random.shuffle(authors)
    authors = ' and '.join(authors)

    #session['username'] = '123@123'


    #Check if user is already logged in (session is set)
    if session.get('username'):

        conn = sqlite3.connect(DATABASE)
        cur = conn.cursor()

        cur.execute("SELECT * FROM user WHERE username = '"+session.get('username')+"';")
        userrow = cur.fetchone()

        # If it's a brand new user signing in - go to quiz
        if userrow is None:
            return render_template("index_quiz.html", authors=authors)

        if userrow[2] and userrow[3] and not userrow[4]:
            myorder = {"cpr":0,"cs":0,"ii":0,"ml":0}
            mypersonalities = userrow[6:]

            ########################################################################
            # -Sum the difference (delta) between class personality and student's
            # personality - for GA, SDP, AI, ML4T, KBAI, AOS, HPC
            ############################################################################

            cpr = ['CS-8803-GA','CS-6601','CS-7641','CS-6475','CS-6476','CS-8803-001']
            cpr_count = len(cpr)

            cs = ['CS-8803-GA','CS-6210','CS-6250','CS-6290','CS-6300','CS-6400','CS-6035','CS-6200','CS-6262',
                  'CS-6291','CS-6310','CS-6340','CSE-6220']
            cs_count = len(cs)

            ii = ['CS-6300','CS-8803-GA','CS-6601','CS-7637','CS-7641','CS-6440','CS-6460','CS-6750']
            ii_count = len(ii)


            ml = ['CS-8803-GA','CS-7641','CS-6476','CS-7642','CS-7646','CSE-6242','CSE-6250']
            ml_count = len(ml)


            cpr_worth = 0
            for f in cpr:
                cpr_worth += quick_value(mypersonalities,f)
            myorder['cpr'] = (1. - 1.*(cpr_worth)/cpr_count) * 100

            cs_worth = 0
            for f in cs:
                cs_worth += quick_value(mypersonalities,f)
            myorder['cs'] = (1. - 1.*(cs_worth)/cs_count) * 100


            ii_worth = 0
            for f in ii:
                ii_worth += quick_value(mypersonalities,f)
            myorder['ii'] = (1. - 1.*(ii_worth)/ii_count) * 100

            ml_worth = 0
            for f in ml:
                ml_worth += quick_value(mypersonalities,f)
            myorder['ml'] = (1. - 1.*(ml_worth)/ml_count) * 100


            myorder2 = [myorder['cpr'],myorder['cs'],myorder['ii'],myorder['ml']]
            order = [i[0] for i in sorted(enumerate(myorder2), key=lambda x:x[1], reverse=True)]

            return render_template("index_specialization.html", authors=authors, worth=myorder2,personality=userrow[6:],
                                   order=order,specs=["Computational Perception & Robotics",
                                                        "Computing Systems",
                                                        "Interactive Intelligence",
                                                        "Machine Learning"])

        if userrow[2] and userrow[3] and userrow[4] and not userrow[5]:
            return render_template("index_generating.html", authors=authors)

        if userrow[5]:
            myclasses = []
            tclass = json.loads(userrow[5])
            tclass.reverse()
            for i in tclass:
                cur.execute("SELECT course,course_name,rating,hours FROM classes WHERE course=?",[str(i)])
                myclasses.append(cur.fetchone())


            when = ["Fall 2018", "Spring 2019", "Fall 2019", "Spring 2020","Fall 2020", "Spring 2021", "Fall 2021", "Spring 2022", "Fall 2022", "Spring 2023"]
            when_count = 0
            myclasses2 = []
            for i in myclasses:
                myclasses2.append([i[0],i[1],i[2],i[3],when[when_count]])
                when_count += 1
                #print(i+(4))

            #cur.execute("SELECT * FROM user WHERE username = '" + session.get('username') + "';")
            #userrow = cur.fetchone()
            return render_template("index_output.html", authors=authors, hours=userrow[2],text=userrow[3][:300],spec=userrow[4],
                                   classes=myclasses2,
                                   personality=userrow[6:])


        return "SOMETHING WENT WRONG...Check with administrators!"
    else:
        return render_template("index.html", authors=authors)
