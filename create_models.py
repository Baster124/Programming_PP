from models_to_migrate import *
import datetime

database.create_all()

user2 = User(iduser=2, username="lix", firstName="Liza", lastName="Karabin", password='asdfasdjklh')
user3 = User(iduser=3, username="viki", firstName="Viktor", lastName="Karabin", password='asdfjddddklh')

bank = Bank(idbank=2, name="Privat", budget=517000)
credit = Credit(idcredit=3, startDate=datetime.datetime(year=2020, month=12, day=31),
                finishDate=datetime.datetime(year=2021, month=12, day=31), sum=20000, percent=30,
              status='opened', User=user, Bank=bank)
credit2 = Credit(idcredit=4, startDate=datetime.datetime(year=2020, month=12, day=31),
                finishDate=datetime.datetime(year=2021, month=12, day=31), sum=20000, percent=30,
                status='opened', User=user3, Bank=bank)
credit3 = Credit(idcredit=5, startDate=datetime.datetime(year=2020, month=12, day=31),
                finishDate=datetime.datetime(year=2021, month=12, day=31), sum=20000, percent=30,
                status='opened', User=user3, Bank=bank)
bank.budget -= credit2.sum
bank.budget -= credit3.sum

database.session.add(user2)
database.session.add(user3)
database.session.add(bank)
database.session.add(credit2)
database.session.add(credit3)
database.session.commit()
