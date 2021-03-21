from flask import Flask, render_template, json, request, session
from db import *

##############################
# app initialization
###############################
app = Flask(__name__)
app.secret_key = "b'\\xb4\\xde\\xd9\\x86\\x93\\xb8\\x1bg\\x93@8W\\xc2&Dn4\\xf4\\xd0\\xa6\\x92\\x13XO'" #str(os.urandom(24)) #randomizing will clear flask_login session when app is restarted
# app.secret_key = str(os.urandom(24))
##############################
# controller initialization
###############################
from controller.index import app_index
from controller.authenticate import app_authenticate
from controller.logout import app_logout
from controller.admin import app_admin
from controller.admin_parse import app_admin_parse
# from controller.admin_ibm import app_admin_ibm
from controller.admin_delete_specs import app_admin_delete_specs
from controller.logic import app_quiz
from controller.logic import app_specialization
from controller.logic import app_generating
from controller.logic import app_hours
from controller.personality_insights import app_personalityInsights
from controller.demo import app_demo

# from controller.testwatson import app_testwatson

app.register_blueprint(app_index)
app.register_blueprint(app_authenticate)
app.register_blueprint(app_logout)
app.register_blueprint(app_admin)
app.register_blueprint(app_admin_parse)
# app.register_blueprint(app_admin_ibm)
app.register_blueprint(app_admin_delete_specs)
app.register_blueprint(app_quiz)
app.register_blueprint(app_specialization)
app.register_blueprint(app_generating)
app.register_blueprint(app_hours)
# app.register_blueprint(app_testwatson)
app.register_blueprint(app_personalityInsights)
app.register_blueprint(app_demo)

if __name__ == "__main__":
    app.run(debug=True, port=80)

