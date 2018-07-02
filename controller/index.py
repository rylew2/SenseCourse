from flask import Blueprint, render_template, session,abort
from db import *
import random
import json

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

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

            conn2 = sqlite3.connect(DATABASE)
            conn2.row_factory = dict_factory
            cur2 = conn2.cursor()

            ########################################################################
            # -Sum the difference (delta) between class personality and student's
            # personality - for each of the 22 personality traits
            ############################################################################

            cur2.execute("SELECT * FROM classes WHERE course = 'CS-8803-GA'")
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
            gadelta = delta1 + delta2 + delta3 + delta4 + delta5 + delta6 + delta7 + delta8 + delta9 + delta10 + delta11 + \
                     delta12 + delta13 + delta14 + delta15 + delta16 + delta17 + delta18 + delta19 + delta20 + delta21 + delta22

            cur2.execute("SELECT * FROM classes WHERE course = 'CS-6300'")
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
            spddelta = delta1 + delta2 + delta3 + delta4 + delta5 + delta6 + delta7 + delta8 + delta9 + delta10 + delta11 + \
                     delta12 + delta13 + delta14 + delta15 + delta16 + delta17 + delta18 + delta19 + delta20 + delta21 + delta22


            cur2.execute("SELECT * FROM classes WHERE course = 'CS-6601'")
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
            aidelta = delta1 + delta2 + delta3 + delta4 + delta5 + delta6 + delta7 + delta8 + delta9 + delta10 + delta11 + \
                     delta12 + delta13 + delta14 + delta15 + delta16 + delta17 + delta18 + delta19 + delta20 + delta21 + delta22

            cur2.execute("SELECT * FROM classes WHERE course = 'CS-7641'")
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
            mldelta = delta1 + delta2 + delta3 + delta4 + delta5 + delta6 + delta7 + delta8 + delta9 + delta10 + delta11 + \
                     delta12 + delta13 + delta14 + delta15 + delta16 + delta17 + delta18 + delta19 + delta20 + delta21 + delta22

            cur2.execute("SELECT * FROM classes WHERE course = 'CS-7637'")
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
            kbdelta = delta1 + delta2 + delta3 + delta4 + delta5 + delta6 + delta7 + delta8 + delta9 + delta10 + delta11 + \
                     delta12 + delta13 + delta14 + delta15 + delta16 + delta17 + delta18 + delta19 + delta20 + delta21 + delta22

            cur2.execute("SELECT * FROM classes WHERE course = 'CS-6210'")
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
            osdelta = delta1 + delta2 + delta3 + delta4 + delta5 + delta6 + delta7 + delta8 + delta9 + delta10 + delta11 + \
                     delta12 + delta13 + delta14 + delta15 + delta16 + delta17 + delta18 + delta19 + delta20 + delta21 + delta22


            cur2.execute("SELECT * FROM classes WHERE course = 'CS-6290'")
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
            hpdelta = delta1 + delta2 + delta3 + delta4 + delta5 + delta6 + delta7 + delta8 + delta9 + delta10 + delta11 + \
                     delta12 + delta13 + delta14 + delta15 + delta16 + delta17 + delta18 + delta19 + delta20 + delta21 + delta22


            if spddelta < gadelta:
                myorder['ii'] += 5

            if aidelta < mldelta:
                myorder['cpr'] += 5
                myorder['ii'] += 5
            else:
                myorder['ml'] += 10

            if kbdelta < aidelta:
                myorder['ii'] += 2
            else:
                myorder['ii'] -= 2

            if kbdelta > mldelta:
                myorder['ii'] += 5
            else:
                myorder['ml'] += 5

            if osdelta < mldelta:
                myorder['cs'] += 5
            else:
                myorder['cs'] -= 5

            if hpdelta < mldelta:
                myorder['cs'] += 5
            else:
                myorder['cs'] -= 5

            myorder2 = [myorder['cpr'],myorder['cs'],myorder['ii'],myorder['ml']]
            order = [i[0] for i in sorted(enumerate(myorder2), key=lambda x:x[1], reverse=True)]
            #print(myorder)
            #print(order)

            return render_template("index_specialization.html", authors=authors, order=order,specs=["Computational Perception & Robotics",
                                                                                                        "Computing Systems",
                                                                                                        "Interactive Intelligence",
                                                                                                        "Machine Learning"])

        if userrow[2] and userrow[3] and userrow[4] and not userrow[5]:
            return render_template("index_generating.html", authors=authors)

        if userrow[5]:
            myclasses = []
            tclass = json.loads(userrow[5])
            for i in tclass:
                cur.execute("SELECT course,course_name,rating,hours FROM classes WHERE course=?",[str(i)])
                myclasses.append(cur.fetchone())

            #cur.execute("SELECT * FROM user WHERE username = '" + session.get('username') + "';")
            #userrow = cur.fetchone()
            return render_template("index_output.html", authors=authors, hours=userrow[2],text=userrow[3][:300],spec=userrow[4],
                                   classes=myclasses,
                                   personality=userrow[6:])


        return "SOMETHING WENT WRONG...Check with administrators!"
    else:
        return render_template("index.html", authors=authors)
