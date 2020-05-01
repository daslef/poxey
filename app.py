from datetime import timedelta
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = '*PInefdlyv5@'
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///users.sqlite3'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.permanent_session_lifetime = timedelta(hours=4)

db = SQLAlchemy(app)


class User(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

    def __str__(self):
        return f"Username - {self.name} Email - {self.email}"


@app.route('/')
def index():
    if session:
        return redirect(url_for("search"))
    return render_template("index.html")


@app.route('/signup', methods=['GET', 'POST'])
def signup():

    if session:
        return redirect(url_for("search"))

    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        found_user = User.query.filter_by(name=username).first()

        if found_user:
            print(found_user)
        else:
            user = User(username, email, password)
            db.session.add(user)
            db.session.commit()
            session['username'] = username
        return redirect(url_for("search"))

    return render_template("signup.html")


@app.route('/signin', methods=['GET', 'POST'])
def signin():

    if session:
        return redirect(url_for("search"))

    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(name=username).first()
        if user and user.password == password:
            session['username'] = username
            return redirect(url_for('search', name=user.name))

    return render_template("signin.html")


@app.route('/profile/<name>', methods=['GET', 'POST'])
def profile(name):
    return render_template("profile.html")


@app.route('/adventure', methods=['GET', 'POST'])
def adventure():
    return render_template("adventure.html")


@app.route('/search', methods=['GET', 'POST'])
def search():
    return render_template("search.html")


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
