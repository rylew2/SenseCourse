from flask import Blueprint, render_template, session, request, jsonify
from db import *
import json
from watson_developer_cloud import PersonalityInsightsV3, WatsonException
import credentials


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


#############################################################################
# /quiz
#  Input: Personal Question from user
# -Run personal against Watson Personality Insights and store in profile
#############################################################################
app_quiz = Blueprint('app_quiz', __name__)


@app_quiz.route("/quiz", methods=['POST'])
def quiz():
    if not session.get('username'):
        return jsonify({'action': 'error', 'type': 'nosession'})

    content = request.get_json()
    _personal = content['personal']

    if _personal == '':
        return jsonify({'action': 'error', 'type': 'personal', 'text': 'You did not answer the question!'})

    if len(_personal.split()) < 4:
        return jsonify({'action': 'error', 'type': 'personal', 'text': 'Please write more!'})

    while len(_personal.split()) < 130:
        _personal += " " + _personal

    conn = sqlite3.connect(DATABASE)

    cur = conn.cursor()
    cur.execute("INSERT INTO user (username, personal) VALUES (?,?);", (session.get('username'), _personal))

    try:
        personality_insights = PersonalityInsightsV3(
            version='2016-10-20',
            username=credentials.username,
            password=credentials.password)

        profile = personality_insights.profile(_personal, content_type="text/plain;charset=utf-8")
    except WatsonException as err:
        return jsonify({'action': 'error', 'type': 'personal', 'text': 'IBM Watson API response: ' + err.message})

    myinsights = {}
    for category in ['needs', 'personality', 'values']:
        # for category in ['needs']:
        for trait in profile[category]:
            myinsights[trait['name']] = trait['percentile']


    #myinsights = {u'Emotional range': 0.28327360777610966, u'Liberty': 0.007254166630536019, u'Extraversion': 0.36721033332928, u'Conservation': 0.0004725338903785459, u'Agreeableness': 0.0167271664796797, u'Harmony': 0.007403095555066019, u'Openness to change': 0.6782749960203265, u'Self-transcendence': 0.36406397019542713, u'Conscientiousness': 0.4783699781762936, u'Hedonism': 0.007182633242991621, u'Self-enhancement': 0.1906140428288537, u'Structure': 0.04808455118475502, u'Practicality': 0.002143384188252162, u'Curiosity': 0.9752422922316606, u'Challenge': 0.3651970174369701, u'Excitement': 0.014951236572620319, u'Love': 0.10285670216713816, u'Self-expression': 0.006274098976008113, u'Closeness': 0.007407496319555118, u'Ideal': 0.07581279455010392, u'Stability': 0.007876238813793346, u'Openness': 0.9999869265760524}

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
                "Selftranscendence = ? WHERE username = ?",
                (myinsights['Challenge'], myinsights['Closeness'], myinsights['Curiosity'],
                 myinsights['Excitement'], myinsights['Harmony'], myinsights['Ideal'],
                 myinsights['Liberty'], myinsights['Love'], myinsights['Practicality'],
                 myinsights['Self-expression'],
                 myinsights['Stability'], myinsights['Structure'], myinsights['Openness'],
                 myinsights['Conscientiousness'], myinsights['Extraversion'], myinsights['Agreeableness'],
                 myinsights['Emotional range'], myinsights['Conservation'], myinsights['Openness to change'],
                 myinsights['Hedonism'], myinsights['Self-enhancement'], myinsights['Self-transcendence'],
                 session.get('username')))

    "Challenge, Closeness, Curiosity, Excitement, Harmony,"
    "Ideal, Liberty, Love, Practicality, Selfexpression,"
    "Stability, Structure, Openness, Conscientiousness, Extraversion,"
    "Agreeableness, Emotionalrange, Conservation, Opennesstochange, Hedonism,"
    "Selfenhancement, Selftranscendence)"

    conn.commit()

    return jsonify({'action': 'ok'})


#############################################################################
# /hours
# Input: time commitment
# -Store hours in profile
#############################################################################
app_hours = Blueprint('app_hours', __name__)


@app_hours.route("/hours", methods=['POST'])
def hours():
    if not session.get('username'):
        return jsonify({'action': 'error', 'type': 'nosession'})

    content = request.get_json()
    _hours = content['hours']

    if _hours == '':
        return jsonify({'action': 'error', 'type': 'hours',
                        'text': 'You did not specify how many hours you want to spend on the course!'})
    if int(_hours) < 5:
        return jsonify({'action': 'error', 'type': 'hours', 'text': 'You specified less than allowed time!'})
    if int(_hours) > 100:
        return jsonify({'action': 'error', 'type': 'hours', 'text': 'You specified more than allowed time!'})

    conn = sqlite3.connect(DATABASE)

    cur = conn.cursor()
    cur.execute("UPDATE user SET hours = '" + _hours + "' WHERE username = '" + session.get('username') + "';")

    conn.commit()

    return jsonify({'action': 'ok'})


#############################################################################
# /specialization
# Take specialization input form user and store in profile
#############################################################################
app_specialization = Blueprint('app_specialization', __name__)


@app_specialization.route("/specialization", methods=['POST'])
def specialization():
    if not session.get('username'):
        return jsonify({'action': 'error', 'type': 'nosession'})

    _specs = request.form['specs']

    if not _specs:
        return jsonify({'action': 'error', 'type': 'noselection', 'text': "You did not pick a specialization!"})

    allspecs = ['Computing Systems', 'Computational Perception & Robotics', 'Interactive Intelligence',
                'Machine Learning']
    if _specs not in allspecs:
        return jsonify({'action': 'error', 'type': 'noexist', 'text': "Something went wrong contact admin!"})

    conn = sqlite3.connect(DATABASE)

    cur = conn.cursor()
    cur.execute("UPDATE user SET specialization = '" + _specs + "' WHERE username = '" + session.get('username') + "';")

    conn.commit()

    return jsonify({'action': 'ok'})


#############################################################################
# /generating
# Generate 10 classes
#############################################################################
app_generating = Blueprint('app_generating', __name__)


@app_generating.route("/generating", methods=['POST'])
def generating():
    if not session.get('username'):
        return jsonify({'action': 'error', 'type': 'nosession'})

    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()

    cur.execute("SELECT * FROM user WHERE username = '" + session.get('username') + "'")
    myrow = cur.fetchone()

    spec = myrow[4]
    myhours = myrow[2]
    mypersonalities = myrow[6:]

    # ['Computing Systems','Computational Perception & Robotics','Interactive Intelligence','Machine Learning']
    classes = []

    # Algorithm

    # GA for ML, Robotics, or Computing Systems, SDP for II
    if (spec == "Machine Learning" or spec == "Computational Perception & Robotics" or spec == "Computing Systems"):
        classes.append("CS-8803-GA")
    else:
        classes.append("CS-6300")

    # Core
    choices_core = {'Machine Learning': ['CS-7641'],
                    'Computational Perception & Robotics': ['CS-6601', 'CS-7641'],
                    'Interactive Intelligence': ['CS-6601', 'CS-7641', 'CS-7637'],
                    'Computing Systems': ['CS-6210', 'CS-6250', 'CS-6290', 'CS-6300', 'CS-6400']}[spec]

    if (spec == "Machine Learning" or spec == "Computational Perception & Robotics"):
        take = 1
    else:
        take = 2

    while take != 0:
        cratings = {}
        chours = {}
        for i in choices_core:
            cur.execute("SELECT rating,hours FROM classes WHERE course = ?", [i])
            myrow = cur.fetchone()
            cratings[i] = myrow[0]
            chours[i] = myrow[1]

        temp_cc = choices_core[:]
        if any(float(k) <= float(myhours) for k in chours.itervalues()):  # eliminate > hours if we can
            for l in choices_core:
                if float(chours[l]) > float(myhours):
                    temp_cc.remove(l)

        bestrating = 0.0
        bestclass = ""
        for l in temp_cc:
            if bestrating < cratings[l]:
                bestrating = cratings[l]
                bestclass = l

        choices_core.remove(bestclass)
        classes.append(bestclass)
        take = take - 1

    # Electives
    choices_core = {'Machine Learning': ['CS-6476', 'CS-7642', 'CS-7646', 'CSE-6242', 'CSE-6250'],
                    'Computational Perception & Robotics': ['CS-6475', 'CS-6476', 'CS-8803-001'],
                    'Interactive Intelligence': ['CS-6440', 'CS-6460', 'CS-6750'],
                    'Computing Systems': ['CS-6035', 'CS-6200', 'CS-6262', 'CS-6291', 'CS-6310', 'CS-6340',
                                          'CSE-6220']}[spec]

    if (spec == "Interactive Intelligence"):
        take = 2
    else:
        take = 3

    while take != 0:
        cratings = {}
        chours = {}
        for i in choices_core:
            cur.execute("SELECT rating,hours FROM classes WHERE course = ?", [i])
            myrow = cur.fetchone()
            cratings[i] = myrow[0]
            chours[i] = myrow[1]

        temp_cc = choices_core[:]
        if any(float(k) <= float(myhours) for k in chours.itervalues()):  # eliminate > hours if we can
            for l in choices_core:
                if float(chours[l]) > float(myhours):
                    temp_cc.remove(l)

        bestrating = 0.0
        bestclass = ""
        for l in temp_cc:
            if bestrating < cratings[l]:
                bestrating = cratings[l]
                bestclass = l

        choices_core.remove(bestclass)
        classes.append(bestclass)
        take = take - 1

    # Generated based on IBM
    # cur.execute("SELECT * FROM classes WHERE course = ?", [i])
    needed = 10 - len(classes)

    conn2 = sqlite3.connect(DATABASE)
    conn2.row_factory = dict_factory
    cur2 = conn2.cursor()

    cur2.execute("SELECT * FROM classes")
    rows = cur2.fetchall()
    new_rows = []
    for i in rows:
        if i['course'] not in classes:
            new_rows.append(i)

    temp = []
    for i in new_rows:
        temp.append(float(i['hours']))

    if sum(1 for i in temp if float(i) <= float(myhours)) > needed:
        nn_rows = []
        for i in new_rows:
            if float(i['hours']) <= float(myhours):
                nn_rows.append(i)
        new_rows = nn_rows

    while needed > 0:
        bestclass = ""
        bestdelta = 999999
        for i in new_rows:
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
            tdelta = delta1 + delta2 + delta3 + delta4 + delta5 + delta6 + delta7 + delta8 + delta9 + delta10 + delta11 + \
                     delta12 + delta13 + delta14 + delta15 + delta16 + delta17 + delta18 + delta19 + delta20 + delta21 + delta22
            if bestdelta > tdelta:
                bestdelta = tdelta
                bestclass = i['course']

        classes.append(bestclass)
        new_rows = [d for d in new_rows if d['course'] != bestclass]
        needed = needed - 1

    json_classes = json.dumps(classes)

    cur.execute("UPDATE user SET generated_classes = '" + json_classes + "' WHERE username = '" + session.get(
        'username') + "';")

    conn.commit()

    return jsonify({'action': 'ok'})
