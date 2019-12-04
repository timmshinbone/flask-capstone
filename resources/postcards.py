import models

from flask import request, jsonify, Blueprint, redirect, url_for
from flask_login import current_user, login_required
from playhouse.shortcuts import model_to_dict

postcards = Blueprint('postcards', 'postcards')


##POSTCARD MODEL FOR REFERENCE
# class Postcard(Model):
# 	drawing = CharField()
# 	message = CharField()
# 	date = DateField(default=datetime.datetime.now())
# 	creator = ForeignKeyField(User, backref='postcards')


#Postcard create route
@postcards.route('/', methods=['POST'])
@login_required
def create_postcard():
	payload = request.get_json()

	postcard = models.Postcard.create(**payload, creator=current_user.id)
	print(postcard.__dict__)
	print(model_to_dict(postcard), "this is postcard model to dict")
	postcard_dict = model_to_dict(postcard)
	postcard_dict['creator'].pop('password')
	postcard_dict['creator'].pop('email')
	return jsonify(data=postcard_dict, status={"code": 201, "message":"Successfully created postcard"}), 201


























