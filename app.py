from flask import Flask, render_template, redirect, request, session
from functools import wraps
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from sqlite3 import connect


app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


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
    
    # checking if user session exists 
    try:
        session["user"]
    except KeyError:
        session["user"] = 0
        
    return render_template('index.html', sesh=session["user"])


@app.route("/menu")
def menu():

    return render_template('menu.html', sesh=session["user"])


@app.route("/gift")
def gift():

    return render_template('giftcards.html', sesh=session["user"])


@app.route("/signin", methods=["GET", "POST"])
def signin():
    
    if request.method == "GET":
        return render_template('signin.html', sesh=session["user"])
    
    if request.method == "POST":
        
        with connect('restaurant.db') as conn:
            
            db = conn.cursor()
            
            username = request.form.get("username")
            password = request.form.get("password")
            
            rows = db.execute("SELECT * FROM users WHERE email=?", [username]).fetchall()
            
            # matching entered credentials with database records
            check = rows[0][2]
            if check_password_hash(check, password):
            
                # setting session id
                session["user"] = rows[0][0]
                print('login successful for ', session["user"])
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
            with connect('restaurant.db') as conn:
            
                db = conn.cursor()
                db.execute('INSERT INTO users (email, hash, name) VALUES (?, ?, ?)', (email, generate_password_hash(pwd), fname + ' ' + lname))
         
        return redirect('/signin')
    
    
@app.route("/user")
def useracc():
    
    with connect('restaurant.db') as conn:
        db = conn.cursor()

        rows = db.execute("SELECT name, email FROM users WHERE id=?", [session["user"]]).fetchall()

        # first name
        name = rows[0][0].split(' ')[0]
        # username
        email = rows[0][1]
        
        return render_template('useracc.html', name=name, username=email, sesh=session["user"])
    

@app.route("/signout")
def signout():
    
    session.clear()
    return redirect('/')
 
app.run()