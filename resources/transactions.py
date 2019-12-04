import models

from flask import request, jsonify, Blueprint, redirect, url_for
from flask_login import current_user, login_required
from playhouse.shortcuts import model_to_dict

transactions = Blueprint('transactions', 'transactions')

##TRANSACTIONS MODEL FOR REFERENCE
# class Transaction(Model):
# 	postcard = ForeignKeyField(Postcard, backref='transactions')
# 	sender = ForeignKeyField(User, backref='transactions')
# 	receiver = ForeignKeyField(User, backref='transactions')
# 	date = DateField(default=datetime.datetime.now())
# 	viewed = BooleanField(default=False)

##Send postcard
@transactions.route('/<p>/<r>', methods=['POST'])
@login_required
def make_transaction(p, r):
	payload = request.get_json()

	payload['postcard'] = models.Postcard.get_by_id(p)
	payload['sender'] = current_user.id
	payload['receiver'] = models.User.get_by_id(r)

	transaction = models.Transaction.create(**payload)
	transaction_dict = model_to_dict(transaction)
	##REMOVE SENSITIVE INFO##################################
	transaction_dict['postcard']['creator'].pop('password')
	transaction_dict['postcard']['creator'].pop('email')
	transaction_dict['sender'].pop('password')
	transaction_dict['sender'].pop('email')
	transaction_dict['receiver'].pop('password')
	transaction_dict['receiver'].pop('email')
	#########################################################
	return jsonify(data=transaction_dict, status={"code": 201, "message":"Success"}), 201


##View all transactions
@transactions.route('/', methods=['GET'])
@login_required
def get_transactions():
	transactions = models.Transaction.select()
	transactions_dicts = [model_to_dict(t) for t in transactions]
	##REMOVE SENSITIVE INFO#################################
	[x['postcard']['creator'].pop('password') for x in transactions_dicts]
	[x['postcard']['creator'].pop('email') for x in transactions_dicts]
	[x['sender'].pop('password') for x in transactions_dicts]
	[x['sender'].pop('email') for x in transactions_dicts]
	[x['receiver'].pop('password') for x in transactions_dicts]
	[x['receiver'].pop('email') for x in transactions_dicts]
	########################################################
	return jsonify(data=transactions_dicts), 200

##View one transaction
@transactions.route('/<id>', methods=['GET'])
def show_one_transaction(id):
	transaction = models.Transaction.get_by_id(id)
	transaction_dict = model_to_dict(transaction)
	##REMOVE SENSITIVE INFO##################################
	transaction_dict['postcard']['creator'].pop('password')
	transaction_dict['postcard']['creator'].pop('email')
	transaction_dict['sender'].pop('password')
	transaction_dict['sender'].pop('email')
	transaction_dict['receiver'].pop('password')
	transaction_dict['receiver'].pop('email')
	#########################################################
	return jsonify(data=transaction_dict, status={"code": 200, 'message':'Found transaction with id{}'.format(transaction.id)})




