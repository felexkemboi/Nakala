import os
from flask import Flask,render_template,request,flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import csv
import psycopg2

#Have pandas installed in your virtual environment  using the command "pip install pandas"
import pandas as pd
import numpy as np

#initialize our app
app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgress@localhost:5432/records'

#initialize the database to our app
db = SQLAlchemy(app)
rows = []
con = "dbname='records' user='postgress' host='localhost' " + \
                  "password='postgress'"
# Create our database schema,,,,,,,you first have to 'flask db init' before, 'flask db migrate' then af
#each time the database models change repeat the migrate and upgrade
migrate = Migrate(app, db)

#Establish a connection to the database
#conn = psycopg2.connect(con)



# Create our database schema
class Data(db.Model):
    __tablename__ = "data"
    id = db.Column(db.Integer, primary_key=True)
    produce_variety = db.Column(db.String(120))
    commodity_type = db.Column(db.String(120))
    unit =           db.Column(db.String(120))
    volume_in_kg =  db.Column(db.Integer)
    value_in_KShs =  db.Column(db.String(120))
    date = 			db.Column(db.DateTime)

#INSERT INTO data("produce_variety","commodity_type","unit","volume_in_kg","date","value_in_KShs")VALUES('Horticulture','Cabbages','Ext Bag',126 ,'1/1/2012 0:00',2205.00 );

@app.route("/test", methods=['GET', 'POST'])
def test():
	dataset = pd.read_csv("Dataset.csv")
	
	with open('Dataset.csv', 'r') as csvFile:
		reader = csv.reader(csvFile)
		headers = next(reader) # for python 2 its reader.next()
		for row in reader:
			#print(row[0],row[1],row[2],row[3],row[4])
			typ = row[4]

			#pick the Kshs column and remove the Kshs string
			typ = typ.replace(typ[:3], '')

			#remove any decimal places to make it an integer to enable it be fed to the database table
			typ = typ.replace(typ[3:], '')

			#create an instance of that that record
			record = Data(produce_variety = row[0],  commodity_type = row[1],  unit = row[2],volume_in_kg =row[3], date=row[5],value_in_KShs=typ)

			#confirm if the record is fed to the database
			print("record added", record)

			#add the record to the database
			db.session.add(record)

			#commit your changes 
			db.session.commit()

			#maybe you redirect the user to other urls
	return render_template('test.html')






@app.route("/home",methods=['GET', 'POST'])
def peana():

	
	#read the from the dataset
	data = Data.query.all()
	return render_template('index.html',data=data)


if __name__ == '__main__':
	app.run(debug=True)

