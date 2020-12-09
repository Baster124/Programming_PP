from migr import database

BaseModel = database.Model


class User(BaseModel):
    __tablename__ = 'user'

    iduser = database.Column(database.INTEGER, primary_key=True)
    username = database.Column(database.VARCHAR(45))
    firstName = database.Column(database.VARCHAR(45))
    lastName = database.Column(database.VARCHAR(45))
    password = database.Column(database.VARCHAR(45))


class Bank(BaseModel):
    __tablename__ = 'bank'

    idbank = database.Column(database.INTEGER, primary_key=True)
    name = database.Column(database.VARCHAR(45))
    budget = database.Column(database.INTEGER)


class Credit(BaseModel):
    __tablename__ = 'credit'

    idcredit = database.Column(database.INTEGER, primary_key=True)
    startDate = database.Column(database.DATETIME)
    finishDate = database.Column(database.DATETIME)
    sum = database.Column(database.INTEGER)
    percent = database.Column(database.INTEGER)
    status = database.Column(database.VARCHAR(45))
    user_iduser = database.Column(database.INTEGER, database.ForeignKey(User.iduser))
    User = database.relationship(User)
    bank_idbank = database.Column(database.INTEGER, database.ForeignKey(Bank.idbank))
    Bank = database.relationship(Bank)


database.create_all()
