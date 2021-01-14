from flask import request, jsonify, json
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
from package import app, db
from package.models import *

auth = HTTPBasicAuth()
with app.app_context():
    Users = User.query.all()
    res = dict()
    for i in range(len(Users)):
        res[Users[i].username] = generate_password_hash(Users[i].password)
    users = jsonify(res)



@auth.verify_password
def verify_password(username, password):
    print(password)
    if username in res and check_password_hash(res.get(username), password):
        return username


@app.route('/')
def main_page():
    return "Hello, World!"


@app.route('/user/', methods=['POST'])
def create_user():
    username = request.json.get('username')
    firstname = request.json.get('firstname')
    lastname = request.json.get('lastname')
    email = request.json.get('email')
    password = request.json.get('password')
    phone = request.json.get('phone')

    user = User.query.filter_by(username=username).first()
    users = User.query.all()
    accounts = Account.query.all()

    if user and user.username == username:
        return jsonify(status='Current user is already exists'), 400
    if username and password and firstname and lastname and email and phone:
        created_acc = Account(id_account=len(accounts) + 1, sum=0)
        created_user = User(id_user=len(users) + 1, username=username, firstname=firstname, lastname=lastname, email=email,
                        password=password, phone=phone, account_id=created_acc.id_account, family_id=-1)
        db.session.add(created_acc)
        db.session.add(created_user)
        db.session.commit()
        result = {
            "data": {
                "id": created_user.id_user,
                "username": created_user.username,
                "firstname": created_user.firstname,
                "lastname": created_user.lastname,
                "email": created_user.email,
                "password": generate_password_hash(created_user.password),
                "phone": created_user.phone,
                "Account": {
                    "id": created_acc.id_account,
                    "sum": created_acc.sum
                }
            },
            "status": "Created"
        }
        res[username] = generate_password_hash(password)
        return jsonify(result), 201
    else:
        return jsonify(status='Bad data'), 400


@app.route('/user/<id>', methods=['GET', 'PUT', 'DELETE'])
@auth.login_required
def userId(id):
    user = User.query.filter_by(id_user=id).first()
    if user is None:
        return jsonify(status='User not found'), 404
    logged_user = auth.current_user()
    if logged_user != user.username:
        return jsonify(status='Access denied'), 403
    account = Account.query.filter_by(id_account=user.account_id).first()
    if request.method == 'GET':
        if user.family_id == -1:
            result = {
                "data": {
                    "id": user.id_user,
                    "username": user.username,
                    "firstname": user.firstname,
                    "lastname": user.lastname,
                    "email": user.email,
                    "password": generate_password_hash(user.password),
                    "phone": user.phone,
                    "Account": {
                        "id": account.id_account,
                        "sum": account.sum
                    }
                },
                "status": "current user"
            }
        else:
            result = {
                "data": {
                    "id": user.id_user,
                    "username": user.username,
                    "firstname": user.firstname,
                    "lastname": user.lastname,
                    "email": user.email,
                    "password": generate_password_hash(user.password),
                    "phone": user.phone,
                    "Account": {
                        "id": account.id_account,
                        "sum": account.sum
                    },
                    "family id": user.family_id
                },
                "status": "current user"
            }
        return jsonify(result), 200

    if request.method == 'PUT':
        username = request.json.get('username')
        firstname = request.json.get('firstname')
        lastname = request.json.get('lastname')
        email = request.json.get('email')
        password = request.json.get('password')
        phone = request.json.get('phone')

        if username or password or firstname or lastname or email or phone:
            if username:
                user.username = username
            if lastname:
                user.lastname = lastname
            if firstname:
                user.firstname = firstname
            if email:
                user.email = email
            if password:
                user.password = password
                res[logged_user] = generate_password_hash(password)
            if phone:
                user.phone = phone

            db.session.query(User).filter_by(id_user=user.id_user).update(
                dict(username=user.username, firstname=user.firstname, lastname=user.lastname,
                     email=user.email, password=user.password, phone=user.phone))
            db.session.commit()
            if user.family_id == -1:
                result = {
                    "data": {
                        "id": user.id_user,
                        "username": user.username,
                        "firstname": user.firstname,
                        "lastname": user.lastname,
                        "email": user.email,
                        "password": generate_password_hash(user.password),
                        "phone": user.phone
                    },
                    "status": "Updated"
                }
            else:
                result = {
                    "data": {
                        "id": user.id_user,
                        "username": user.username,
                        "firstname": user.firstname,
                        "lastname": user.lastname,
                        "email": user.email,
                        "password": generate_password_hash(user.password),
                        "phone": user.phone,
                        "family id": user.family_id
                    },
                    "status": "Updated"
                }

            return jsonify(result), 201
        else:
            return jsonify(status='Bad request'), 400

    if request.method == 'DELETE':
        finances = Finances.query.all()
        for i in range(len(finances)):
            if finances[i].account_id == user.account_id:
                db_session1 = db.session.object_session(finances[i])
                db_session1.delete(finances[i])
                db_session1.commit()
        db_session1 = db.session.object_session(user)
        db_session1.delete(user)
        db_session1.commit()

        db_session2 = db.session.object_session(account)
        db_session2.delete(account)
        db_session2.commit()
        return jsonify(status='deleted'), 200


@app.route('/family/', methods=['POST'])
def create_fam():
    surname = request.json.get('surname')

    families = Family.query.all()
    if surname:
        created_fam = Family(id_family=len(families) + 1, surname=surname, budget=0)
        db.session.add(created_fam)
        db.session.commit()
        result = {
            "data": {
                "id": created_fam.id_family,
                "surname": created_fam.surname,
                "budget": created_fam.budget,
            }
        }
        return jsonify(result), 201
    else:
        return jsonify(status='Bad data'), 400


@app.route('/family/<id>', methods=['GET', 'PUT', 'DELETE'])
@auth.login_required
def family__id(id):
    logged_user = auth.current_user()

    family = Family.query.filter_by(id_family=id).first()
    if family is None:
        return jsonify(status='Family not found'), 404

    users = User.query.filter(User.family_id == id).all()
    k = 0
    for u in users:
        if u.username != logged_user:
            k += 1
    if k == len(users):
        return jsonify(status='Access denied'), 403
    result = {
        "data": {
            "id": family.id_family,
            "surname": family.surname,
            "budget": family.budget,
        }
    }
    if request.method == 'GET':

        return jsonify(result), 200

    if request.method == 'PUT':
        surname = request.json.get('surname')

        if surname:
            family.surname = surname
            db.session.query(Family).filter_by(id_family=family.id_family).update(
                dict(surname=family.surname))
            db.session.commit()
            return jsonify(status="Updated", id=family.id_family, surname=family.surname, budget=family.budget), 200
        else:
            return jsonify(status='Bad request'), 400

    if request.method == 'DELETE':
        users = User.query.all()
        for i in range(len(users)):
            if users[i].family_id == int(id):
                db.session.query(User).filter_by(id_user=users[i].id_user).update(
                    dict(family_id=-1))
                db.session.commit()
        transactions = Transaction.query.all()
        for i in range(len(transactions)):
            if transactions[i].family_id == int(id):
                db_session1 = db.session.object_session(transactions[i])
                db_session1.delete(transactions[i])
                db_session1.commit()
        db_session2 = db.session.object_session(family)
        db_session2.delete(family)
        db_session2.commit()
        return jsonify(status='deleted'), 200


@app.route('/family/<id>/members/', methods=['GET'])
@auth.login_required
def getfamilymembers(id):
    logged_user = auth.current_user()

    family = Family.query.filter_by(id_family=id).first()
    if family is None:
        return jsonify(status='Family not found'), 404

    users = User.query.filter(User.family_id == id).all()
    k = 0
    for u in users:
        if u.username != logged_user:
            k += 1
    if k == len(users):
        return jsonify(status='Access denied'), 403

    courses_list = []
    for cor in users:
        courses_list.append(User.get_users2(cor))
    if len(courses_list) == 0:
        return jsonify(status='There are no users in this family'), 404
    else:
        return jsonify(courses_list), 200




@app.route('/family/<familyId>/<accountId>', methods=['POST'])
@auth.login_required
def transaction(familyId, accountId):
    family = Family.query.filter_by(id_family=familyId).first()
    account = Account.query.filter_by(id_account=accountId).first()
    if family is None:
        return jsonify(status='Family not found'), 404
    if account is None:
        return jsonify(status='User with this account id not found'), 404

    logged_user = auth.current_user()
    users = User.query.filter(User.family_id == familyId).all()
    k = 0
    for u in users:
        if u.username != logged_user:
            k += 1
        else:
            cur_user = u
    if k == len(users):
        return jsonify(status='You are not a family member'), 403
    if cur_user.account_id != int(accountId):
        return jsonify(status='It is not your account'), 403

    transactions = Transaction.query.all()
    direction = request.json.get('direction')
    money = request.json.get('money')

    if direction != 1 and direction != 0:
        return jsonify(status='You can have only f_to_p or p_to_f direction'), 400
    if money > 0:
        if direction == 1 and family.budget > money:
            family.budget -= money
            account.sum += money
            db.session.query(Family).filter_by(id_family=family.id_family).update(
                dict(budget=family.budget))
            db.session.commit()
            db.session.query(Account).filter_by(id_account=account.id_account).update(
                dict(sum=account.sum))
            db.session.commit()
        elif direction == 0 and account.sum > money:
            family.budget += money
            account.sum -= money
            db.session.query(Family).filter_by(id_family=family.id_family).update(
                dict(budget=family.budget))
            db.session.query(Account).filter_by(id_account=account.id_account).update(
                dict(sum=account.sum))
            db.session.commit()
        else:
            return jsonify(status="Not enough money to make a transaction"), 400

        create_trans = Transaction(id_transaction=len(transactions) + 1, money=money,
                                   direction=direction, family_id=familyId, account_id=accountId)

        db.session.add(create_trans)
        db.session.commit()
        return jsonify(status="Transaction completed", id=create_trans.account_id, money=create_trans.money,
                direction=create_trans.direction, family_id=create_trans.family_id, account_id=create_trans.account_id), 200
    else:
        return jsonify(status='Bad request'), 400


@app.route('/family/<familyId>/member/<userId>/', methods=['PUT', 'DELETE'])
@auth.login_required
def add_or_delete_member(familyId, userId):
    family = Family.query.filter_by(id_family=familyId).first()
    user = User.query.filter_by(id_user=userId).first()
    if family is None:
        return jsonify(status='Family not found'), 404
    if user is None:
        return jsonify(status='User not found'), 404

    logged_user = auth.current_user()
    users = User.query.filter(User.family_id == familyId).all()
    k = 0
    for u in users:
        if u.username != logged_user:
            k += 1
        else:
            cur_user = u
    if k == len(users):
        return jsonify(status='You are not a family member'), 403

    if request.method == 'PUT':
        if user.family_id == int(familyId):
            return jsonify(status='This user is already in the family'), 400
        else:
            db.session.query(User).filter_by(id_user=userId).update(
                dict(family_id=familyId))
            db.session.commit()
            return jsonify(status='User was added to the family'), 200
    else:
        if user.family_id == -1:
            return jsonify(status='This user does not belong to any family'), 400
        else:
            db.session.query(User).filter_by(id_user=userId).update(
                dict(family_id=-1))
            db.session.commit()
            return jsonify(status='User was deleted from family')


@app.route('/family/<familyId>/transactions', methods=['GET'])
@auth.login_required
def get_trans(familyId):
    family = Family.query.filter_by(id_family=familyId).first()
    if family is None:
        return jsonify(status='Family not found'), 404

    logged_user = auth.current_user()
    users = User.query.filter(User.family_id == familyId).all()
    k = 0
    for u in users:
        if u.username != logged_user:
            k += 1
        else:
            cur_user = u
    if k == len(users):
        return jsonify(status='You are not a family member'), 403

    fam_transactions = Transaction.query.filter(Transaction.family_id == familyId).all()
    transaction_list = []
    if not len(fam_transactions):
        return jsonify(status='This family have no transactions'), 404
    else:
        for trans in fam_transactions:
            transaction_list.append(Transaction.get_transaction(trans))
        return jsonify(transaction_list), 200



@app.route('/user/account/<accountId>/transactions', methods=['GET'])
@auth.login_required
def getacc_trans(accountId):
    account = Account.query.filter_by(id_account=accountId).first()
    if account is None:
        return jsonify(status='Account not found'), 404

    user = User.query.filter_by(account_id=accountId).first()
    logged_user = auth.current_user()
    if logged_user != user.username:
        return jsonify(status='Access denied'), 403


    acc_transactions = Transaction.query.filter(Transaction.account_id == accountId).all()
    acc_finances = Finances.query.filter(Finances.account_id == accountId).all()
    transaction_list = []
    if not len(acc_transactions) and not len(acc_finances):
        return jsonify(status='This account have no transactions and finances'), 404
    else:
        for trans in acc_transactions:
            transaction_list.append(Transaction.get_transaction(trans))
        for trans in acc_finances:
            transaction_list.append(Finances.get_finances(trans))
        return jsonify(transaction_list), 200


@app.route('/user/account/<accountId>/purchase', methods=['POST'])
@auth.login_required
def finan(accountId):
    account = Account.query.filter_by(id_account=accountId).first()
    if account is None:
        return jsonify(status='Account not found'), 404

    user = User.query.filter_by(account_id=accountId).first()
    logged_user = auth.current_user()
    if logged_user != user.username:
        return jsonify(status='Access denied'), 403

    finances = Finances.query.all()
    item = request.json.get('item')
    price = request.json.get('price')
    date = request.json.get('date')
    status = request.json.get('status')
    if status != 'expenses' and status != 'incomes':
        return jsonify(status='You can have only expenses or incomes status'), 400
    if item and price and date and status:
        if price < 0:
            return jsonify(status='Bad data'), 400
        created_fin = Finances(id_fin=len(finances) + 1, item=item, price=price, date=date, account_id=accountId, status=status)
        if status == 'expenses':
            if price > account.sum:
                return jsonify(status='Not enough money'), 400
            account.sum -= price
        else:
            account.sum += price
        db.session.query(Account).filter_by(id_account=accountId).update(
            dict(sum=account.sum))
        db.session.add(created_fin)
        db.session.commit()
        result = {
            "Account": {
                "id": account.id_account,
                "sum": account.sum
            },
            "status": "OK"
        }
        return jsonify(result), 200
    else:
        return jsonify(status='Bad data'), 400


@app.route('/users/', methods=['GET'])
# @auth.login_required(role='teacher')
def create_all_users():
    users = User.query.all()
    courses_list = []
    for cor in users:
        courses_list.append(User.get_users(cor))
    if len(courses_list) == 0:
        return jsonify(status='Users not found'), 404
    else:
        return jsonify(courses_list), 200

