import datetime
from flask import Flask, render_template, request, redirect, url_for, session, flash
from sqlalchemy.exc import IntegrityError
from models import add_user, check_user

app = Flask(__name__)
app.secret_key = '*PInefdlyv5@'


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/registration', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        add_user(username, email, password)
    return render_template("signup.html")


if __name__ == "__main__":
    app.run(debug=True)
