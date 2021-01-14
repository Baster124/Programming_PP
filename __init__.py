from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'secret key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://{user}:{password}@{server}/{database}'.format(
    user='root', password='tworichdragonsassets', server='localhost', database='cshflw')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.debug = True
db = SQLAlchemy(app)
client = app.test_client()
engine = db.engine
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
SessionFactory = sessionmaker(bind=engine)

from package import models, routes
