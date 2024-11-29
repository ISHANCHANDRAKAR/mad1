#starting of the app
from flask import Flask

app=None

def setup_app():
	app=Flask(__name__)
	app.debug=True

	app.app_context().push() #Direct access to other modules
	print("HomeEase is started .... ")

#Call the setup
setup_app()

# Import all the controllers so they are loaded
from application.controllers import *


if __name__=="__main__":
	app.run(debug=True)