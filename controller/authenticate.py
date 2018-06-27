from flask import Blueprint, render_template, session, abort, request, jsonify
from db import *
from validate_email import validate_email

app_authenticate = Blueprint('app_authenticate',__name__)

@app_authenticate.route("/register", methods = ['POST'])
def register():
    if session.get('username'):
        return jsonify({'action': 'ok'})
   
    _username = request.form['inputUsername']
    _password = request.form['inputPassword']
    if _username == '':
        return jsonify({'action': 'error', 'type': 'username',
                        'text': 'Empty username is not allowed'})
    if not validate_email(_username):
        return jsonify({'action': 'error', 'type': 'username',
                        'text': 'Not a valid email address'})
    
    if _password == '':
        return jsonify({'action': 'error', 'type': 'password',
                        'text': 'Empty password is not allowed'})

    if len(_password) <= 5:
        return jsonify({'action': 'error', 'type': 'password',
                        'text': 'Password must be at least 6 characters'})

    conn = sqlite3.connect(DATABASE)
    
    cur = conn.cursor()
    
    cur.execute("SELECT * FROM login WHERE username = '"+_username+"'")
    myrow = cur.fetchone()
    
    if myrow is None: #NO LOGINS EXIST with such username
        cur.execute("INSERT INTO login (username, password, admin) VALUES ('"+_username+"', '"+_password+"', 0)")
        conn.commit()
        session['username'] = _username
        session['admin'] = False
        return jsonify({'action': 'ok'})
    
    
    #1 is username #2 is password
    if myrow[2] == _password:
        session['username'] = _username
        if myrow[3]:
            session['admin'] = True
        else:
            session['admin'] = False
        return jsonify({'action': 'ok'})
        
    return jsonify({'action': 'error', 'type': 'password',
                        'text': 'User already exists but incorrect password'})


