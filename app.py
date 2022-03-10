from flask import Flask, render_template, redirect, request
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3


app = Flask(__name__)

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


@app.route("/signin", methods=["POST", "GET"])
def signup():
    
    if request.method == "GET":
        return render_template('signin.html')
        
        
    if request.method == "POST":
        
        # retrieve info from form
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        email = request.form.get('email')
        
        # phone = request.form.get('phone')
        pwd = request.form.get('pwd')
        c_pwd = request.form.get('c_pwd')
        
        
        if pwd == c_pwd:
            
            with sqlite3.connect('restaurant.db', check_same_thread=False) as conn:
            
                db = conn.cursor()
                db.execute('INSERT INTO users (email, hash, name) VALUES (?, ?, ?)', (email, generate_password_hash(pwd), fname + ' ' + lname))
                #db.commit()
                
        return redirect('/menu')
    
 
app.run()