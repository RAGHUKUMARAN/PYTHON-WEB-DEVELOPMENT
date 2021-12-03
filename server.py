from flask import Flask,render_template,url_for, redirect, request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user-data.db'

db = SQLAlchemy(app)

class User(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	username = db.Column(db.String(25), unique=True, nullable=False)
	password = db.Column(db.String(20), nullable = False)

db.create_all()

@app.route("/")
def home():
	return redirect(url_for('register_page'))

@app.route('/login', methods = ["POST","GET"])
def login_page():
	if request.method == "POST":
		user = User.query.filter_by(username = request.form['username']).first()
		if user != None:
			if user.password == request.form['password']:
				return redirect(url_for('success_page'))
			print("[!]Incorrect password")
		else:
			print("[-]User unavailable")
	return render_template('form.html',form_title="Login Form")


@app.route('/register', methods = ["POST","GET"])
def register_page():
	if request.method == "POST":
		username = request.form['username']
		password = request.form['password']
		user = User.query.filter_by(username = username).first()
		if user == None:
			user = User(username = username,password = password)
			db.session.add(user)
			db.session.commit()
			return redirect(url_for('success_page'))
		print("[!]User Already available")
	return render_template('form.html',form_title="Register Form")

@app.route("/success")
def success_page():
	return render_template("success.html")

if __name__== "__main__":
	app.run(debug=True)
