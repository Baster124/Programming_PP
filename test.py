from models import *
import datetime

db.create_all()

user = User(iduser=1, userName="yarko", firstName="Yaroslav", password='asdfjklh' , lastName="Karabin")
bank = Bank(idbank=2, name="Privat", budget=517000)
credit = Credit(idcredit=3,
                startDate=datetime.datetime(year=2020, month=12, day=31),
                finishDate=datetime.datetime(year=2021, month=12, day=31),
                sum=20000,
                percent=30,
                status='opened',
            )

db.session.add(user)
db.session.add(bank)
db.session.add(credit)

db.session.commit()