from flask import Blueprint, request, jsonify
from app.helpers.Account import Account
from app.helpers.Response import Response
from app.helpers.Auth import login_required, admin_required
import re

accounts = Blueprint('accounts', __name__)

@accounts.route('/accounts', methods=['GET'])
@login_required
def get_accounts():

    per_page = int(request.args.get('per_page')) if 'per_page' in request.args else 5
    page = int(request.args.get('page')) if 'page' in request.args else 1

    qFirstName = request.args.get('firstName') if 'firstName' in request.args else None
    qGender = request.args.get('gender') if 'gender' in request.args else None
    qLastName = request.args.get('lastName') if 'lastName' in request.args else None
    qEmail = request.args.get('email') if 'email' in request.args else None
    qBalance = int(request.args.get('balance')) if 'balance' in request.args else None
    qAccountNumber = int(request.args.get('accountNumber')) if 'accountNumber' in request.args else None
    qCity = request.args.get('city') if 'city' in request.args else None
    qState = request.args.get('state') if 'state' in request.args else None
    qEmployer = request.args.get('employer') if 'employer' in request.args else None
    qAddress = request.args.get('address') if 'address' in request.args else None

    search_criteria = {}
    if qFirstName is not None:
        search_criteria["firstname"] = {"$regex": re.escape(qFirstName) + r".*"}
    if qGender is not None:
        search_criteria["gender"] = qGender
    if qLastName is not None:
        search_criteria['lastname'] = {"$regex":  re.escape(qLastName) + r".*"}
    if qEmail is not None:
        search_criteria['email'] = {"$regex": r".*" + re.escape(qEmail) + r".*"}
    if qBalance is not None:
        search_criteria['balance'] = {'$eq': qBalance}
    if qAccountNumber is not None:
        search_criteria['account_number'] = {'$eq': qAccountNumber}
    if qCity is not None:
        search_criteria['city'] = {"$regex": r".*" + re.escape(qCity) + r".*"}
    if qState is not None:
        search_criteria['state'] = {"$regex": r".*" + re.escape(qState) + r".*"}
    if qEmployer is not None:
        search_criteria['employer'] = {"$regex": r".*" + re.escape(qEmployer) + r".*"}
    if qAddress is not None:
        search_criteria['address'] = {"$regex": r".*" + re.escape(qAddress) + r".*"}

    sort_criteria = {}
    sort_criteria['sortDirection'] = int(request.args.get('sortDirection'))
    sort_criteria['sortExpression'] = request.args.get('sortExpression')

    accounts, pagination = Account.get_page_accounts(page, per_page, search_criteria, sort_criteria)

    result = {
        'pagination': {
            'total': pagination.total,
            'per_page': pagination.per_page,
            'current_page': pagination.current_page,
            'last_page': pagination.last_pages,
            'prev_page': pagination.prev_page,
            'next_page': pagination.next_page,
            'from': pagination.start,
            'to': pagination.end,
            'base_url': request.url
        },
        'accounts': accounts
    }

    return Response.make_response(result, 200)

@accounts.route('/account/<int:account_number>', methods=['GET'])
@login_required
def get_single_account(account_number):
    account = Account.find_account(account_number)

    if account:
        resp = Response.make_response({'data': Account.make_account_data(account)}, 200)
    else:
        resp = Response.make_response({'message': 'Account Not Found'}, 404)
    return resp

@accounts.route('/accounts', methods=['POST'])
@admin_required
def create_account():
    json_data = request.get_json()
    result = Account.create_account(json_data)

    if result:
        return Response.make_response({'message': 'Account created'}, 200)
    else:
        return Response.make_response({}, 400)

@accounts.route('/account/<int:account_number>', methods=['DELETE'])
@admin_required
def delete_account(account_number):
    account = Account.find_account(account_number)

    if account:
        Account.delete_account(account_number)
        resp = Response.make_response({'message': 'Account {} deleted'.format(account_number)}, 200)
    else:
        resp = Response.make_response({'message': 'Account not found'}, 404)
    return resp

@accounts.route('/account/<int:account_number>', methods=['POST'])
@admin_required
def update_account(account_number):
    json_data = request.get_json()

    account = Account.find_account(account_number)

    if account:
        Account.update_account(account_number, json_data)

        resp = Response.make_response({'message': 'Account {} updated'.format(account_number)}, 200)
    else:
        resp = Response.make_response({'message': 'Account not found'}, 404)
    return resp

@accounts.route('/exist', methods=['POST'])
def account_number_exist():
    json_data = request.get_json()
    if 'account_number' in json_data:
        account_number = json_data['account_number']
        account = Account.find_account(account_number)
    elif 'email' in json_data:
        email = json_data['email']
        account = Account.find_account_by_email(email)

    if account:
        return Response.make_response({'exist': True}, 200)
    else:
        return Response.make_response({'exist': False}, 200)
