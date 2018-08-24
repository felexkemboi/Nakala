
#   BELOW IS WHAT I WAS ABLE TO DO IN THE 20HRS GIVEN FOR THE CHALLENGE
#   NAKALA
# Setting up flask app  with a postgress

The below article will cover the steps to be followed when setting up  the whole app. This is more like a documentation of what i was able to do and what i was not able to do and will have out of sequence instructions or solutions to errors so read thoroughly.

# # # #What i was able to do
1.I first created a virtualenv using python3

2.Activated the virtulenv then installed flask

3.Got postgress installed in my laptop so it is all about creating the table

4.Copied the csv file you shared to the same directory with app.py

5.Read the data from the csv file,each row and presented it as a list

6.Loop through the list and get each item,read it as cell,then feed each cell to the database


I was able to import the data from the csv file to a postgress table

Was not able to create interface for the user to interact with the above data

# # # #What is to be done
1. Create a function to render a template with varoius  buttons e.g  to show data for a specific day,data for a certain range of prices,give the user ability to query for a specific range of data and so many as long as they are required

2.APIs-this could involve creation of endpoints as stipulated in our problem statement
I will need atleast 4 days to fully develop the system as per your requirement.If possible you could give me another 4 days to finish up the task.

That was what i was able to do for the 20hrs given.

-Meanwhile you can check the code snippet below or see the raw code in my [Repository](</https://github.com/felexkemboi/Nakala/>)



## Setting up a database

You'll need the packages.You can check on your virtual environment by the command ##pip freeze 

```alembic==1.0.0
click==6.7
Flask==1.0.2
Flask-Migrate==2.2.1
Flask-SQLAlchemy==2.3.2
itsdangerous==0.24
Jinja2==2.10
Mako==1.0.7
MarkupSafe==1.0
numpy==1.15.1
pandas==0.23.4
psycopg2==2.7.5
python-dateutil==2.7.3
python-editor==1.0.3
pytz==2018.5
six==1.11.0
SQLAlchemy==1.2.11
Werkzeug==0.14.1
```


#### Bare minimum files

Since its a simple app,all the code is in a single file **app.py**
~~~~
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

# Create our database schema,,,,,,,you first have to 'flask db init' before, 'flask db migrate' then af
#each time the database models change repeat the migrate and upgrade
migrate = Migrate(app, db)

#Establish a connection to the database
#conn = psycopg2.connect(con)

"""
python manage.py db init
python manage.py db migrate
python manage.py db upgrade
"""

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


	#read the from the database
	data = Data.query.all()
	return render_template('index.html',data=data)


if __name__ == '__main__':
	app.run(debug=True)




~~~~

