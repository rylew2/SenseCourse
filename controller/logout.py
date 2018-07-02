from flask import Blueprint, session, redirect


app_logout = Blueprint('app_logout',__name__)

#############################################################################
# /logout
# Clear session and redirect to home page (index.html)
#############################################################################
@app_logout.route("/logout", methods = ['GET','POST'])
def logout():
    session.clear()
    return redirect("/")
