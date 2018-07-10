from flask import Blueprint, render_template, session, abort, request, jsonify, redirect
from db import *

app_demo = Blueprint('app_demo', __name__)


#############################################################################
# /demo
# Creates a demo of the course!
#############################################################################
@app_demo.route("/demo", methods=['GET'])
def admin():
    authors = ["Andrey Makhanov", "Ryan Lewis"]
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()

    cur.execute("SELECT * FROM user WHERE username = 'demo@demo';")
    userrow = cur.fetchone()

    myclasses = []
    tclass = json.loads(userrow[5])

    if userrow[4] == "Computing Systems":
        smart_cnt = 4
        # 6 courses
    else:
        smart_cnt = 5
        # 5 courses

    tclass.reverse()
    for i in tclass:
        cur.execute("SELECT course,course_name,rating,hours FROM classes WHERE course=?", [str(i)])
        myclasses.append(cur.fetchone())

    when = ["Fall 2018", "Spring 2019", "Fall 2019", "Spring 2020", "Fall 2020", "Spring 2021", "Fall 2021", "Spring 2022",
            "Fall 2022", "Spring 2023"]
    when_count = 0
    myclasses2 = []
    for i in myclasses:
        zcnt = 0
        if when_count < smart_cnt:
            zcnt = 1
        myclasses2.append([i[0], i[1], i[2], i[3], when[when_count], zcnt])
        when_count += 1
        # print(i+(4))

    # cur.execute("SELECT * FROM user WHERE username = '" + session.get('username') + "';")
    # userrow = cur.fetchone()
    return render_template("index_output.html", authors=authors, hours=userrow[2], text=userrow[3][:300], spec=userrow[4],
                           classes=myclasses2,
                           personality=userrow[6:])
