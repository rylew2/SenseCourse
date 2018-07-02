from flask import Blueprint, render_template, session, abort, request, jsonify,redirect
from db import *
from validate_email import validate_email

app_admin = Blueprint('app_admin',__name__)


#############################################################################
# /admin
# Administrator view. Display all table data.
#############################################################################
@app_admin.route("/admin", methods = ['GET'])
def admin():
    if not session.get('username'):
        return redirect("/", code=302)

    #if not session.get('username'):
    #    return "Cannot Authenticate! Not an admin user"

    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()

    cur.execute("SELECT name FROM sqlite_master WHERE type = 'table';")
    tables = cur.fetchall()


    cur.execute("SELECT * FROM login;")
    logins_names = list(map(lambda x: x[0], cur.description))
    logins = cur.fetchall()

    cur.execute("SELECT * FROM user;")
    user_names = list(map(lambda x: x[0], cur.description))
    user = cur.fetchall()

    cur.execute("SELECT * FROM classes;")
    classes_names = list(map(lambda x: x[0], cur.description))
    classes = cur.fetchall()

    return render_template("admin.html",tables=tables,
                           logins_names=logins_names, logins=logins,
                           user_names=user_names,user=user,
                           classes_names=classes_names,classes=classes,
                           authors="Andrey Makhanov and Ryan Lewis")
