import os
from flask import Flask,render_template,request,flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


#Have pandas installed in your virtual environment  using the command "pip install pandas"
import pandas as pd

#initialize our app
app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:root@localhost:5432/records'

#initialize the database to our app
db = SQLAlchemy(app)


# Create our database schema,,,,,,,you first have to 'flask db init' before, 'flask db migrate' then af
#each time the database models change repeat the migrate and upgrade
migrate = Migrate(app, db)

# Create our database schema
class Data(db.Model):
    __tablename__ = "data"
    id = db.Column(db.Integer, primary_key=True)
    produce_variety = db.Column(db.String(120))
    commodity_type = db.Column(db.String(120))
    unit =           db.Column(db.String(120))
    volume_in_kg =  db.Column(db.String(120))
    date = 			db.Column(db.DateTime)



@app.route("/test",methods=['GET', 'POST'])
def test():
	#read the from the dataset
	data = pd.read_csv("Dataset.csv")
	#data = Data.query.all()
	return render_template('test.html',data=data)

@app.route("/home",methods=['GET', 'POST'])
def peana():
	#read the from the dataset
	data = Data.query.all()
	return render_template('index.html',data=data)
@app.route("/data", methods=['POST','GET'])
def data():
	return '''committed!Z!'''


@app.route("/feed", methods=['GET', 'POST'])
def feed():
	
	return render_template('mimi.html')


@app.route("/yes")
def connect():
	return "i like what i am seeing"


if __name__ == '__main__':
	app.run(debug=True)

