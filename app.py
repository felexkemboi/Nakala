import os
from flask import Flask,render_template,request,flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import csv


#Have pandas installed in your virtual environment  using the command "pip install pandas"
import pandas as pd
import numpy as np

#initialize our app
app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:root@localhost:5432/records'

#initialize the database to our app
db = SQLAlchemy(app)
rows = []

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
    volume_in_kg =  db.Column(db.Integer)
    value_in_KShs =  db.Column(db.Integer)
    date = 			db.Column(db.DateTime)

#INSERT INTO data(produce_variety,commodity_type,unit,volume_in_kg,date,value_in_KShs)VALUES('Horticulture','Cabbages','Ext Bag',126 , 2205.00 ,'1/1/2012 0:00');

@app.route("/test", methods=['GET', 'POST'])
def test():
	dataset = pd.read_csv("Dataset.csv")
	
	with open('Dataset.csv', 'r') as csvFile:
		reader = csv.reader(csvFile)
		headers = next(reader) # for python 2 its reader.next()
		for row in reader:
			#print(row[0],row[1],row[2],row[3],row[4])
			record = Data(id =id,produce_variety = row[0],  commodity_type = row[1],  unit = row[2],volume_in_kg =row[3], date=row[4])
			print("record adde", record)
			db.session.add(record)
			db.session.commit()
			print("record added")
			#data = Data.query.all()
	return render_template('test.html',data=rows)






@app.route("/home",methods=['GET', 'POST'])
def peana():
	#read the from the dataset
	data = Data.query.all()
	return render_template('index.html',data=data)


if __name__ == '__main__':
	app.run(debug=True)

