import os
from peewee import *
from flask_login import UserMixin
import datetime

from playhouse.db_url import connect

if 'ON_HEROKU' in os.environ:
	DATABASE= connect(os.environ.get('DATABASE_URL'))
else:
	DATABASE = SqliteDatabase('postcard.sqlite')

class User(UserMixin, Model):
	username = CharField(unique = True)
	password = CharField()
	email = CharField(unique = True)

	class Meta:
		database = DATABASE

class Friendship(Model):
	user_one = ForeignKeyField(User, backref='friendships')
	user_two = ForeignKeyField(User, backref='friendships')
	status = IntegerField(default=0) 
			#0 for pending, 
			#1 for friends, 
			#2 for declined, 
			#3 for blocked, 

	class Meta:
		database = DATABASE


class Postcard(Model):
	drawing = CharField()
	message = CharField()
	date = DateTimeField(default=datetime.datetime.now)
	creator = ForeignKeyField(User, backref='postcards')

	class Meta:
		database = DATABASE


class Transaction(Model):
	postcard = ForeignKeyField(Postcard, backref='transactions')
	sender = ForeignKeyField(User, backref='transactions')
	receiver = ForeignKeyField(User, backref='transactions')
	date = DateTimeField(default=datetime.datetime.now)
	viewed = BooleanField(default=False)

	class Meta:
		database = DATABASE


def initialize():
	DATABASE.connect()
	DATABASE.create_tables([User, Friendship, Postcard, Transaction], safe=True)
	print("TABLES Created")
	DATABASE.close()










