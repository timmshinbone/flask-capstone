from flask import Flask, jsonify, g
from flask_cors import CORS
from flask_login import LoginManager

import models


DEBUG = True
PORT = 8000

app = Flask(__name__)

app.secret_key = "this is the secret key"

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(userid):
	try:
		return models.User.get(models.User.id == userid)
	except models.DoesNotExist:
		return None

@login_manager.unauthorized_handler
def unauthorized():
	return jsonify(data={'error':'You must be logged in to view this page'}, status={'code':401, 'message':'You must be logged in to access that resource'}), 401


@app.before_request
def before_request():
	#connect to db before each request
	g.db = models.DATABASE
	g.db.connect()

@app.after_request
def after_request(response):
	#closes db connection after each request
	g.db.close()
	return response




if __name__ == '__main__':
	models.initialize()
	app.run(debug=DEBUG, port=PORT)