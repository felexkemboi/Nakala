#   NAKALA
# Setting up flask app  with a postgress 

The below article will cover the steps to be followed when setting up  the whole app. This is more like a documentation of what i was able to do and what i was not able to do and will have out of sequence instructions or solutions to errors so read thoroughly.



## Setting up a database

You'll need the packages 

```alembic
alembic
Flask-Migrate
Flask-Script
Flask-SQLAlchemy
psycopg2
```

Now. Information. alembic will install on its own if you install the 3 packages after it. You'll need `psycopg2` **ONLY IF** you plan on deploying to heroku and using their database.

You'll need at least 3 files to use migration and other features of `flask-migrate`



#### Bare minimum files

Since its a simple app,all the code is in a single file **app.py**
~~~~
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

"""
python manage.py db init
python manage.py db migrate
python manage.py db upgrade
"""

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



@app.route("/db", methods=['GET', 'POST'])
def test():
	dataset = pd.read_csv("Dataset.csv")
	
	with open('Dataset.csv', 'r') as csvFile:
		reader = csv.reader(csvFile)
		headers = next(reader) # for python 2 its reader.next()
		for row in reader:
			#print(row[0],row[1],row[2],row[3],row[4])
			record = Data(id =id,produce_variety = row[0],  commodity_type = row[1],  unit = row[2],volume_in_kg =row[3],                                   date=row[4])
			
	return render_template('test.html',data=rows)






@app.route("/home",methods=['GET', 'POST'])
def peana():
	#read the from the dataset
	data = Data.query.all()
	return render_template('index.html',data=data)

@app.route("/feed", methods=['GET', 'POST'])
def feed():
	return render_template('mimi.html')


@app.route("/yes")
def connect():
	return "i like what i am seeing"


if __name__ == '__main__':
	app.run(debug=True)


~~~~

