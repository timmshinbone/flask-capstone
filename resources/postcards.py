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

#postcard index(show all) route
@postcards.route('/', methods=['GET'])
@login_required
def get_all_postcards():
	postcards = models.Postcard.select()
	postcard_dicts = [model_to_dict(p) for p in postcards]

	[x['creator'].pop('password') for x in postcard_dicts]
	[x['creator'].pop('email') for x in postcard_dicts]

	return jsonify(data=postcard_dicts), 200

#show only one postcard route
@postcards.route('/<id>', methods=['GET'])
@login_required
def get_one_postcard(id):
	postcard = models.Postcard.get_by_id(id)
	postcard_dict = model_to_dict(postcard)
	postcard_dict['creator'].pop('password')
	postcard_dict['creator'].pop('email')
	return jsonify(data=postcard_dict, status={"code": 200, "message":"Found Postcard with id{}".format(postcard.id)}), 200






















