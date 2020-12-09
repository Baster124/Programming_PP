from migrate import db
from werkzeug.security import generate_password_hash

Base = db.Model


class User(Base):

    iduser = db.Column(db.INTEGER, primary_key=True, autoincrement=True )
    userName = db.Column(db.VARCHAR(45))
    firstName = db.Column(db.VARCHAR(45))
    password = db.Column(db.VARCHAR(128))
    lastName = db.Column(db.VARCHAR(45))


    def __init__(self, iduser, userName, firstName, password, lastName):
        self.iduser = iduser
        self.userName = userName
        self.firstName = firstName
        self.password = generate_password_hash(password)
        self.lastName = lastName


class Bank(Base):

    idbank = db.Column(db.INTEGER, primary_key=True , autoincrement=True)
    name = db.Column(db.VARCHAR(45))
    budget = db.Column(db.INTEGER)


class Credit(Base):


    idcredit = db.Column(db.INTEGER, primary_key=True , autoincrement=True)
    startDate = db.Column(db.DATETIME)
    finishDate = db.Column(db.DATETIME)
    sum = db.Column(db.INTEGER)
    percent = db.Column(db.INTEGER)
    status = db.Column(db.VARCHAR(45))
    userId = db.Column(db.INTEGER, db.ForeignKey(User.iduser))
    bankId = db.Column(db.INTEGER, db.ForeignKey(Bank.idbank))

db.create_all()
# from migrate import db
# from werkzeug.security import generate_password_hash
#
# Base = db.Model
#
#
# class User(Base):
#     __tablename__ = 'user'
#
#     iduser = db.Column(db.INTEGER, primary_key=True)
#     userName = db.Column(db.VARCHAR(45))
#     firstName = db.Column(db.VARCHAR(45))
#     password = db.Column(db.VARCHAR(128))
#     lastName = db.Column(db.VARCHAR(45))
#

# class Bank(Base):
#     __tablename__ = 'bank'
#
#     idbank = db.Column(db.INTEGER, primary_key=True)
#     name = db.Column(db.VARCHAR(45))
#     budget = db.Column(db.INTEGER)
#
#
# class Credit(Base):
#     __tablename__ = 'credit'
#
#     idcredit = db.Column(db.INTEGER, primary_key=True)
#     startDate = db.Column(db.DATETIME)
#     finishDate = db.Column(db.DATETIME)
#     sum = db.Column(db.INTEGER)
#     percent = db.Column(db.INTEGER)
#     status = db.Column(db.VARCHAR(45))
#     userId = db.Column(db.INTEGER, db.ForeignKey(User.iduser))
#     User = db.relationship(User)
#     bankId = db.Column(db.INTEGER, db.ForeignKey(Bank.idbank))
#     Bank = db.relationship(Bank)
#
# db.create_all()