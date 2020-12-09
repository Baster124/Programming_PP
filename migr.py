from flask import Flask
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'secret key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://{user}:{password}@{server}/{database}'.format(
    user='root', password='tworichdragonsassets', server='localhost', database='crediteservice')



app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
manager = Manager(app)
database = SQLAlchemy(app)
migrate = Migrate(app, database)
manager.add_command('database', MigrateCommand)

engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])

SessionFactory = sessionmaker(bind=engine)

BaseModel = declarative_base()
