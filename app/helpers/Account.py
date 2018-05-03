from app import mongo
from app.helpers.Pagination import Pagination
from collections import OrderedDict
import pymongo
import numbers
import re

class Account:


    @staticmethod
    def get_page_accounts(page, per_page, search_criteria, sort_criteria):
        total = mongo.db.accounts.find(search_criteria).count()
        pagination = Pagination(total, page, per_page)

        accounts = mongo.db.accounts.find(search_criteria).sort(sort_criteria['sortExpression'], sort_criteria['sortDirection']).skip(pagination.start - 1).limit(per_page)

        page_accounts = []

        for account in accounts:
            page_accounts.append(Account.make_account_data(account))

        return page_accounts, pagination


    @staticmethod
    def find_all():
        accounts = mongo.db.accounts.find()
        list_accounts = []
        for account in accounts:
            list_accounts.append(Account.make_account_data(account))
        return list_accounts

    @staticmethod
    def delete_account(account_number):
        mongo.db.accounts.delete_one({'account_number': account_number})

    @staticmethod
    def find_account(account_number):
        account = mongo.db.accounts.find_one({'account_number': account_number})
        return account

    @staticmethod
    def create_account(data):
        account_data = Account.make_account_data(data)

        print(isinstance(account_data['balance'], numbers.Number))
        print (isinstance(account_data['age'], numbers.Number))
        print(re.match(r"^[a-z]+[a-z0-9._]+@[a-z]+\.[a-z.]{2,5}$", account_data['email']))

        if isinstance(account_data['balance'], numbers.Number) == False or account_data['balance'] < 0:
            return False

        if isinstance(account_data['age'], numbers.Number) == False or account_data['age'] < 0:
            return False

        if not re.match(r"^[a-z]+[a-z0-9._]+@[a-z]+\.[a-z.]{2,5}$", account_data['email']):
            return False

        if Account.find_account(account_data['account_number']):
            return False

        if Account.find_account_by_email(account_data['email']):
            return False

        mongo.db.accounts.insert_one(account_data)
        return True

    @staticmethod
    def update_account(account_number, data):
        account_data = Account.make_account_data(data)
        account_data['account_number'] = account_number

        mongo.db.accounts.update_one({'account_number': account_number}, {'$set': account_data}, upsert=False)

    @staticmethod
    def make_account_data(account):
        properties = ['account_number', 'balance', 'firstname', 'lastname',
                      'age', 'gender', 'address', 'employer', 'email', 'city', 'state']
        account_data = {}
        for p in properties:
            if p in account:
                account_data[p] = account[p]
        return account_data

    @staticmethod
    def find_account_by_email(email):
        account = mongo.db.accounts.find_one({'email': email})
        return account

