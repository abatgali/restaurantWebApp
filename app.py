from flask import Flask, render_template, redirect, request
from functools import wraps
#from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3


app = Flask(__name__)

class session(object):
    
    def __init__(self) -> None:
        pass

# to disable caching
@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
def index():

    return render_template('index.html')


@app.route("/menu")
def menu():

    return render_template('menu.html')


@app.route("/gift")
def gift():

    return render_template('giftcards.html')


@app.route("/signin", methods=["GET", "POST"])
def signin():
    
    if request.method == "GET":
        return render_template('signin.html')
    
    if request.method == "POST":
        
        with sqlite3.connect('restaurant.db', check_same_thread=False) as conn:
            
            db = conn.cursor()
            
            username = request.form.get("username")
            password = request.form.get("password")
            
            rows = db.execute("SELECT * FROM users WHERE email=?", [username])
            # matching entered credentials with database records
            check = rows.fetchall()[0][2]
            session = rows.fetchall()[0]
            if check_password_hash(check, password):
                print('login successful')
                return redirect('/user')
            
            else:
                return redirect("/menu")


@app.route("/signup", methods=["POST"])
def signup():
        
    if request.method == "POST":
        
        # retrieve info from form
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        email = request.form.get('email')
        
        # phone = request.form.get('phone')
        pwd = request.form.get('pwd')
        c_pwd = request.form.get('c_pwd')
        
        
        if pwd == c_pwd:
            
            # opening connection to database and committing the newly created account
            with sqlite3.connect('restaurant.db', check_same_thread=False) as conn:
            
                db = conn.cursor()
                db.execute('INSERT INTO users (email, hash, name) VALUES (?, ?, ?)', (email, generate_password_hash(pwd), fname + ' ' + lname))

                
        return render_template('/signin')
    
@app.route("/user")
def useracc():
    
    with sqlite3.connect('restaurant.db', check_same_thread=False) as conn:
            
        db = conn.cursor()
        
        db.execute("SELECT ")
    return render_template('useracc.html')
 
app.run()