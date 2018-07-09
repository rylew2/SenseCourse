from flask import Blueprint, render_template, session, abort, request, jsonify, redirect

app_demo = Blueprint('app_demo', __name__)


#############################################################################
# /demo
# Creates a demo of the course!
#############################################################################
@app_demo.route("/demo", methods=['GET'])
def admin():
    session['username'] = "demo@demo"
    session['admin'] = False
    return redirect("/", code=302)
