from flask import request, jsonify, json
from werkzeug.security import generate_password_hash, check_password_hash
from Package import app, db
from Package.models import *

from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)

with app.app_context():
    Users = User.query.all()
    username_table = {i.username: i for i in Users}
    password_table = {i.password: i for i in Users}
    userid_table = {i.iduser: i for i in Users}


def authenticate(username, password):
    user = username_table.get(username, None)
    if user and safe_str_cmp(user.password.encode('utf-8'), password.encode('utf-8')):
        return user


def identity(payload):
    user_id = payload['identity']
    return userid_table.get(user_id, None)


@app.route('/login/', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"Status": "Missing JSON in request"}), 400

    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if not username:
        return jsonify({"Status": "Missing username parameter"}), 400
    if not password:
        return jsonify({"Status": "Missing password parameter"}), 400
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({"Status": "User not found"}), 404

    if password == user.password:
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"Status": "Bad password"}), 401


@app.route('/user/', methods=['POST'])
def create_user():
    username = request.json.get('username')
    firstname = request.json.get('firstname')
    lastname = request.json.get('lastname')
    password = request.json.get('password')

    user = User.query.filter_by(username=username).first()
    users = User.query.all()

    if user and user.username == username:
        return jsonify(status='Current user is already exists'), 400
    if username and password and firstname and lastname:
        created_user = User(iduser=len(users) + 1, username=username, firstname=firstname, lastname=lastname,
                        password=password)
        db.session.add(created_user)
        db.session.commit()
        result = {
            "data": {
                "id": created_user.iduser,
                "username": created_user.username,
                "firstname": created_user.firstname,
                "lastname": created_user.lastname,
                "password": created_user.password,
            },
            "status": "Created"
        }
        return jsonify(result), 201
    else:
        return jsonify(status='Bad data'), 400



@app.route('/user/<int:id>', methods=['GET', 'PUT', 'DELETE'])
@jwt_required
def userId(id):
    user = User.query.filter_by(iduser=id).first()
    if user is None:
        return jsonify(status='not found user'), 404
    current_user = get_jwt_identity()
    if current_user != user.username:
        return jsonify(status='Access denied'), 403
    if request.method == 'GET':
        return jsonify(status='current User', name=user.username, firstname=user.firstname, lastname=user.lastname), 200

    if request.method == 'PUT':
        username = request.json.get('username', None)
        password = request.json.get('password', None)
        firstname = request.json.get('firstname', None)
        lastname = request.json.get('lastname', None)

        if username and password and firstname and lastname:
            user.username = username
            user.lastname = lastname
            user.firstname = firstname
            user.password = password
            db.session.commit()
            return jsonify(status='updated', name=user.username, firstname=user.firstname, lastname=user.lastname), 202
        else:
            return jsonify(status='Bad data'), 204
    if request.method == 'DELETE':
        db.session.execute(f'''DELETE FROM user WHERE {id}=iduser; ''')
        return jsonify(status='deleted'), 201
    else:
        return jsonify('User not found'), 404


@app.route('/credit/<id_user>', methods=['POST'])
@jwt_required
def create_credit(id_user):
    user = User.query.filter_by(iduser=id_user).first()
    current_user = get_jwt_identity()
    if current_user != user.username:
        return jsonify(status='Access denied'), 403

    startdate = request.json.get('startdate', None)
    finishdate = request.json.get('finishdate', None)
    sum = request.json.get('sum', None)
    percent = request.json.get('percent', None)
    status = request.json.get('status', None)
    bank = Bank.query.filter_by(name='Privat').first()
    bank_id = bank.idbank


    if bank.budget < sum:
        return jsonify({"can't get credit": "badget of bank is empty", "status": "Bad request"}), 400
    credits = Credit.query.all()
    if startdate and finishdate and sum and percent and status:
        new_credit = Credit(startDate=startdate, finishDate=finishdate, sum=sum, percent=percent, status=status,
                            bankId=bank_id, userId=id_user, idcredit=len(credits)+1)
        db.session.add(new_credit)
        db.session.commit()
        result = {
            "data": {
                "startDate": startdate,
                "finishDate": finishdate,
                "sum": sum,
                "percent": percent,
                "status": status,
                "bank_name": bank.name
            },
            "status": "Created"
        }
        return jsonify(result), 201
    else:
        return jsonify(status='Bad data'), 204


@app.route('/credit/<int:id_user>/<int:id>/', methods=['GET', 'PUT'])
@jwt_required
def creditId(id_user, id):
    user = User.query.filter_by(iduser=id_user).first()
    current_user = get_jwt_identity()

    credit = Credit.query.filter_by(idcredit=id).first()
    if current_user != user.username or credit.userId != id_user:
        return jsonify(status='Access denied'), 403
    
    if credit is None:
        return jsonify(status='not found Credit'), 404
    if request.method == 'GET':
        return jsonify(status='current Credit', startdate=credit.startDate, finishdate=credit.finishDate,
                       sum=credit.percent, status_of_credite=credit.status), 200

    if request.method == 'PUT':
        startdate = request.json.get('startdate', None)
        finishdate = request.json.get('finishdate', None)
        sum = request.json.get('sum', None)
        percent = request.json.get('percent', None)
        status = request.json.get('status', None)

        if startdate and finishdate and sum and percent and status:
            credit.startDate = startdate
            credit.finishDate = finishdate
            credit.sum = sum
            credit.percent = percent
            credit.status = status
            #   return 200
            db.session.commit()
            return jsonify(status='updated', startdate=credit.startDate, finishdate=credit.finishDate, sum=credit.sum,
                           percent=credit.percent, statusc=credit.status), 202
        else:
            return jsonify(status='Bad data'), 204

