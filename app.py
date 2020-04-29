import datetime
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = '*PInefdlyv5@'
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///users.sqlite3'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

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
    return render_template("index.html")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        found_user = User.query.filter_by(name=username).first()
        
        if found_user:
            print(found_user)
        else:
            usr = User(username, email, password)
            db.session.add(usr)
            db.session.commit()
        return redirect(url_for("index"))
        
    return render_template("signup.html")
    

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
