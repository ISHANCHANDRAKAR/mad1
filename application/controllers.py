#App routes
from flask import Flask,render_template
from flask import current_app as app

#Many controllers/routers here 

@app.route("/")
def home():
	return render_template("index.html")