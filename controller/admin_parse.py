from flask import Blueprint, render_template
import os
import json
from pprint import pprint


from db import *

app_admin_parse = Blueprint('app_admin_parse',__name__)


################################################################################################################
# /admin_parse
# Run once at start.
#  - Generates class reviews (ourcourses.json) from raw OMSCentral data (anonymized-backup.json)
#  - Generates concatenated course reviews for each class (reviews.json) from class reviews (ourcourses.json)
###############################################################################################################
@app_admin_parse.route("/admin_parse", methods = ['GET','POST'])
def admin_parse():
    log = "<pre>"
    our_courses = []

    with open('anonymized-backup.json') as f:
        data = json.load(f)

    courses = data['courses']
    for i in courses:
        if courses[i]["average"]["rating"] != 0 and not i.startswith("MGT") and not i.startswith("ISYE"):
            our_courses.append(i)

    with open('courses.json') as f:
        coursedata = json.load(f)

    #Generate Rating
    new_courses = {}
    for i in our_courses:
        temp = {}
        temp['rating'] = courses[i]['average']['rating']
        temp['workload'] = courses[i]['average']['workload']
        temp['coursename'] = coursedata[i]["name"]
        new_courses[i] = temp
   


    with open('ourcourses.json', 'w') as outfile:
        json.dump(new_courses, outfile, indent=4, sort_keys=True)


    # Generate Reviews for classes:
    reviews = data['reviews']

    new_reviews = {}
    for i in our_courses:
        new_reviews[i] = ""

    for i in reviews:
        if reviews[i]["course"] in our_courses and 'rating' in reviews[i] and reviews[i]['rating'] >= 4:
            this_course = reviews[i]["course"]
            new_reviews[this_course] += " " + reviews[i]["text"]

    with open('reviews.json', 'w') as outfile:
        json.dump(new_reviews, outfile, indent=4, sort_keys=True)

    log += str(len(our_courses))
    log += str(len(new_courses))
    log += str(len(new_reviews)) + "\r\n"
    #pprint(new_courses)
    log += "\r\nDONE"
    log += "</pre>"
    return log
