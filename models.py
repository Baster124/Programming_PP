from migr import db

Base = db.Model


class Account(Base):
    __tablename__ = "account"
    id_account = db.Column(db.INTEGER, primary_key=True)
    sum = db.Column(db.INTEGER, nullable=True)


class Finances(Base):
    __tablename__ = "finances"
    id_fin = db.Column(db.INTEGER, primary_key=True)
    item = db.Column(db.VARCHAR(45))
    price = db.Column(db.INTEGER)
    date = db.Column(db.DATETIME(10))
    account_id = db.Column(db.INTEGER, db.ForeignKey(Account.id_account))
    Account = db.relationship(Account)
    status = db.Column(db.VARCHAR(45))

    def get_finances(self):
        result = {
            'id': self.id_fin,
            'item': self.item,
            'price': self.price,
            'date': self.date,
            'status': self.status
        }
        return result


class Family(Base):
    __tablename__ = "family"

    id_family = db.Column(db.INTEGER, primary_key=True)
    surname = db.Column(db.VARCHAR(45), nullable=True)
    budget = db.Column(db.INTEGER)


class User(Base):
    __tablename__ = "user"

    id_user = db.Column(db.INTEGER, primary_key=True)
    username = db.Column(db.VARCHAR(45), nullable=True)
    firstname = db.Column(db.VARCHAR(45))
    lastname = db.Column(db.VARCHAR(45))
    email = db.Column(db.VARCHAR(45))
    password = db.Column(db.VARCHAR(45), nullable=True)
    phone = db.Column(db.VARCHAR(45))
    account_id = db.Column(db.INTEGER, db.ForeignKey(Account.id_account))
    Account = db.relationship(Account)
    family_id = db.Column(db.INTEGER, db.ForeignKey(Family.id_family), nullable=True)
    Family = db.relationship(Family)

    def get_users(self):
        result = {
            'id': self.id_user,
            'username': self.username,
            'password': self.password,
            'family id': self.family_id,
            'account id': self.account_id
        }
        return result

    def get_users2(self):
        result = {
            'id': self.id_user,
            'username': self.username,
            'family id': self.family_id,
            'account id': self.account_id
        }
        return result


class Transaction(Base):
    __tablename__ = "transactiondata"

    id_transaction = db.Column(db.INTEGER, primary_key=True)
    money = db.Column(db.INTEGER, nullable=True)
    direction = db.Column(db.INTEGER, nullable=True)
    family_id = db.Column(db.INTEGER, db.ForeignKey(Family.id_family))
    Family = db.relationship(Family)
    account_id = db.Column(db.INTEGER, db.ForeignKey(Account.id_account))
    Account = db.relationship(Account)

    def get_transaction(self):
        result = {
            'id': self.id_transaction,
            'money': self.money,
            'direction': self.direction,
            'family id': self.family_id,
            'account id': self.account_id
        }
        return result


db.create_all()
