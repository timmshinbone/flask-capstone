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


@transactions.route('/<p>/<r>', methods=['POST'])
@login_required
def make_transaction(p, r):
	payload = request.get_json()

	payload['postcard'] = models.Postcard.get_by_id(p)
	payload['sender'] = current_user.id
	payload['receiver'] = models.User.get_by_id(r)

	transaction = models.Transaction.create(**payload)
	transaction_dict = model_to_dict(transaction)

	return jsonify(data=transaction_dict, status={"code": 201, "message":"Success"}), 201










