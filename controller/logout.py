from flask import Blueprint, session, redirect


app_logout = Blueprint('app_logout',__name__)

@app_logout.route("/logout", methods = ['GET','POST'])
def logout():
    session.clear()
    return redirect("/")
