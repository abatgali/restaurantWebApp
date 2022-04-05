#from asyncio.windows_events import NULL
from ast import excepthandler
import sqlite3
from urllib import response
from flask import Flask, render_template, redirect, request, session
from functools import wraps
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from sqlite3 import connect
import json

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


@app.route("/menu", methods=['GET','POST'])
def menu():
    
    
    if request.method == 'GET':

        with connect('restaurant.db') as conn:
            db = conn.cursor()
            
            # retrieve menu items 
            res = db.execute('SELECT * FROM menu').fetchall()
            # print(res)

            # to compose menu json from db
            menu = {}
            # cycling through categories
            for i in range(1, 14):
                
                catg = db.execute('SELECT type FROM category WHERE id=?', [i]).fetchall()[0][0]
                
                items = {}
                for j in res:
                    
                    if i == j[1]:
                        
                        # print(j)
                        # item id at j[0]
                        # category at j[1]
                        
                        item = {}
                        
                        result = db.execute('SELECT * FROM items WHERE id = ?', [j[0]]).fetchall()[0]
                        name = result[1]
                        item["price"] = result[2]
                        item["desc"] = result[3]
                        item["id"] = result[0]
                        
                        # appending each item to items dict
                        items.update({name: item})
                        #print(item["id"])
                
                # adding category and its items to the menu 
                # with each cycle of nested loop                        
                menu[catg] = items
   
            #print(menu)
                        
            print('\n----------------------')
                
            """  with open('menu_cleaned.json', 'r') as items:
            menu = json.load(items)
            print(menu) """
            
            # adding selected items by the user to a list
            # to show in the cart
            if not (request.args.get('id') is None):
                
                id = request.args.get('id')
                # checking if cart has items 
                try:
                    session["cart"]

                    if id in session["cart"]:
                        session["cart"][id] += 1
                    else:
                        session["cart"].update({id:1})
                    print(session["cart"])
                    
                # if not, starting count
                except KeyError:
                    
                    session["cart"].update({id:1})
                    
            
        return render_template('menu.html', sesh=session["user"], menu=menu)


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
            # print(rows)
            check = rows[0][2]
            if check_password_hash(check, password):
            
                # setting session id
                session["user"] = rows[0][0]
                # setting cart empty
                session["cart"] = {}
                print('login successful for ', session["user"])
                return redirect('/user')
            
            else:
                
                msg = "Login failed. Incorrect username or password provided."
                return render_template('error.html', msg=msg)


@app.route("/signup", methods=["POST"])
def signup():
        
    if request.method == "POST":
        
        # retrieve info from form
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        email = request.form.get('email')
        
        # opening connection to database and committing the newly created account
        with connect('restaurant.db') as conn:
            
            db = conn.cursor()
            
            result = db.execute('SELECT email FROM users WHERE email = ?', [email]).fetchall()
            
            print(result, len(result))
            
            # phone = request.form.get('phone')
            pwd = request.form.get('pwd')
            c_pwd = request.form.get('c_pwd')
            
            if pwd == c_pwd:
                
                try:
                    db.execute('INSERT INTO users (email, hash, name) VALUES (?, ?, ?)', (email, generate_password_hash(pwd), fname + ' ' + lname))
                except:
                    return render_template('error.html', msg="Username already in use.", sesh=session["user"])
            
            else:
                return render_template('error.html', msg="Passwords didn't match.", sesh=session["user"])
                
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
    
    
@app.route("/cart", methods=['GET','POST'])
def cart():
            
    if len(session["cart"]) != 0:
        
        with connect('restaurant.db') as conn:
            db = conn.cursor()
            
            # storing prices for every selected item
            prices = {}
            subtotal = 0
            for id in session["cart"]:
                prices.update({id:db.execute('SELECT price, item FROM items WHERE id=?', [id]).fetchall()[0]}) 

                subtotal += prices[id][0] * session["cart"][id]
            
            tax = round(0.07 * subtotal, 2)
            subtotal = round(subtotal, 2)
            # print(prices)
            
            # confirming the order
            if request.method == "POST":
                
                place_order(tax, subtotal)
                
                return render_template('confirm.html')
            
    else:
        prices = {}
        subtotal = 0
        tax = 0

    return render_template('cart.html', cart=session["cart"], prices=prices, subtotal=subtotal, tax=tax)


@app.route("/inquire", methods=['POST', 'GET'])
def contactus():
    if request.method == "POST":
        email = request.form.get('email')
        inquiry = request.form.get('question')
        
    return render_template('inquire.html')


@app.route("/signout")
def signout():
    
    session.clear()
    return redirect('/')


@app.route("/error")
def error(msg="What did you do!?"): 
    
    return render_template('error.html', msg=msg)


def place_order(tax, subtotal):
    

    with connect('restaurant.db') as conn:
        db = conn.cursor()
        
        db.execute('INSERT INTO orders (userID, selectedItems, subtotal, tax, total) VALUES (?, ?, ?, ?, ?)', (session["user"], json.dumps(session["cart"]), subtotal, tax, round(subtotal+tax, 2)))
    
    return 

 
app.run()