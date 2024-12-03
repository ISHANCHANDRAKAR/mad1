#starting of the app
from flask import Flask
from application.models import db 

app=None

def setup_app():
	app=Flask(__name__)
	app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///home_ease.sqlite3" #Have db file
	app.debug=True
	app.secret_key = "very much much strongest pass"
	db.init_app(app) #Flask app connected to db(SQL alchemy)
	app.app_context().push() #Direct access to other modules
	print("HomeEase is started .... ")

#Call the setup
setup_app()

# Import all the controllers so they are loaded
from application.controllers import *


if __name__=="__main__":
	app.run(debug=True)


app.secret_key = "something only you know"
