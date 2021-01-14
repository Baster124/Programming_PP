from migr import db
from flask import Flask
from flask_jwt import JWT, jwt_required, current_identity
from werkzeug.security import safe_str_cmp
Base = db.Model


class User(Base):
    iduser = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    username = db.Column(db.VARCHAR(45))
    firstname = db.Column(db.VARCHAR(45))
    password = db.Column(db.VARCHAR(128))
    lastname = db.Column(db.VARCHAR(45))

    def __init__(self, iduser, username, firstname, password, lastname):
        self.iduser = iduser
        self.username = username
        self.firstname = firstname
        self.password = password
        self.lastname = lastname


class Bank(Base):
    idbank = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    name = db.Column(db.VARCHAR(45))
    budget = db.Column(db.INTEGER)


class Credit(Base):
    idcredit = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    startDate = db.Column(db.DATETIME)
    finishDate = db.Column(db.DATETIME)
    sum = db.Column(db.INTEGER)
    percent = db.Column(db.INTEGER)
    status = db.Column(db.VARCHAR(45))
    userId = db.Column(db.INTEGER, db.ForeignKey(User.iduser))
    bankId = db.Column(db.INTEGER, db.ForeignKey(Bank.idbank))


db.create_all()