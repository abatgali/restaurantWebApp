from flask import Flask, render_template, redirect

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

@app.route("/giftcards")
def giftcards():

    return render_template('giftcards.html')

@app.route("/signin")
def signin():

    return render_template('signin.html')

app.run()