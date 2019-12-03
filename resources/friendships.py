import models

from flask import request, jsonify, Blueprint
from flask_login import current_user, login_required
from playhouse.shortcuts import model_to_dict

friendships = Blueprint('friendships', 'friendships')

##FRIENDSHIP MODEL FOR REFERENCE
# class Friendship(Model):
# 	user_one = ForeignKeyField(User, backref='friendships')
# 	user_two = ForeignKeyField(User, backref='friendships')
# 	status = IntegerField(default=0) 

#make a friend request
@friendships.route('<user1>/<user2>', methods=['POST'])
@login_required
def make_friend_request(user1, user2):
	payload = request.get_json()

	print("THIS IS THE PAYLOAD OF THE FRIEND REQ", payload)

	payload['user_one'] = current_user.id
	payload['user_two'] = models.User.get_by_id(user2)

	friendship = models.Friendship.create(**payload)
	friendship_dict = model_to_dict(friendship)
	friendship_dict['user_one'].pop('password')
	friendship_dict['user_one'].pop('email')
	friendship_dict['user_two'].pop('password')
	friendship_dict['user_two'].pop('email')


	return jsonify(data=friendship_dict, status={"code":201, "message": "Success"}), 201

#show all friend requests
@friendships.route('/', methods=['GET'])
def show_all_friendships():
	friendships = models.Friendship.select()
	print(friendships, "this is the friend requests")
	friendships_dicts = [model_to_dict(f) for f in friendships]

	[x['user_one'].pop('password') for x in friendships_dicts]
	[x['user_one'].pop('email') for x in friendships_dicts]
	[x['user_two'].pop('password') for x in friendships_dicts]
	[x['user_two'].pop('email') for x in friendships_dicts]

	return jsonify(data=friendships_dicts), 200


#show one friend request
@friendships.route('/<id>', methods=['GET'])
def show_one_friendships(id):
	friendship = models.Friendship.get_by_id(id)
	print(friendship, "this is the friend request")
	friendship_dict = model_to_dict(friendship)

	friendship_dict['user_one'].pop('password')
	friendship_dict['user_one'].pop('email')
	friendship_dict['user_two'].pop('password')
	friendship_dict['user_two'].pop('email')

	return jsonify(data=friendship_dict, status={"code": 200, 'message':'Found friend request with id{}'.format(friendship.id)}), 200









