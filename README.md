#   NAKALA
# Setting up flask app  with a postgress sql

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


~~~~python
from manage import db,app

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)

    def __repr__(self):
        return '<User %r>' % (self.nickname)
~~~~



2. 

~~~python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'

db = SQLAlchemy(app)

from models import User

@app.route('/add/')
def webhook():
    name = "ram"
    email = "ram@ram.com"
    u = User(id = id, nickname = name, email = email)
    print("user created", u)
    db.session.add(u)
    db.session.commit()
    return "user created"

@app.route('/delete/')
def delete():
    u = User.query.get(i)
    db.session.delete(u)
    db.session.commit()
    return "user deleted"

if __name__ == '__main__':
    app.run()
~~~



3. **manage.py**

~~~~python
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from app import app, db

migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
~~~~



**NOTE**: Where we are importing what. In **app.py** we are importing User after we declare `db` since that is used in models, from where User is imported.



#### Database configuration params

~~~~python
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
~~~~

This sets up the parameter `SQLALCHEMY_DATABASE_URI` and tells it to point to a sqlite db. This can also be declared in a `config.py` file and then in **app.py**

~~~~python
app.config.from_object('config')
~~~~





## flask-migrate

Initialize the database and create the migrations folder.





### Force flask-migrate to detect changes in data types of columns

Check [https://stackoverflow.com/questions/17174636/can-alembic-autogenerate-column-alterations]

The above one worked. But very importantly also check [https://stackoverflow.com/questions/33944436/flask-migrate-and-changing-column-type]



## Deploying on Heroku

Heroku has a free hobby development database that we can use happily. Let's see how we can set up the database, link it to our app and do the necessary stuff keeping most of our hair intact.



### Step 1

`psycopg2` required from here on.

Go to this [https://devcenter.heroku.com/articles/getting-started-with-python#provision-a-database]

Also check this out [https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xviii-deployment-on-the-heroku-cloud]

*Do note the above link is outdated in regards to the command given for adding a database. It is now `hobby-dev` not `dev`. Also we don't need to promote now. It will already be promoted to `DATABASE_URL`*

Run the below command on terminal. 

~~~~
heroku addons:add heroku-postgresql:hobby-dev
~~~~

### Step 2

**2.1.** Now we'll face some problem regarding migrating. What we'll do is below in order to bypass the problems.

~~~~
heroku run python
>> import os
>> os.environ.get('DATABASE_URL')
~~~~

It will give the link to the development database on Heroku. (It will be something like *postgres://bllahblah*)

**2.2.** Replace the value of `DATABASE_URI` in config.py with this value.

**2.3.**Then do apply your changes to Heroku database.

~~~
python manage.py db init
python manage.py db migrate
python manage.py db upgrade
~~~

Then push your code as usual. Better push your migrations on Heroku too. Don't leave your migrations folder out of git commit. But keep local sqlite db outside.

### Step 3 | Procfile

~~~~
web: python manage.py runserver --host 0.0.0.0 --port ${PORT}
init: python manage.py db init
migrate: python manage.py db migrate
upgrade: python manage.py db upgrade
~~~~

This is how the Procfile **MUST** look like. We don't care much about the last 3. The first one is what is very very important. Notice in **app.py** we a calling `app.run()` without any parameters (host and port). It should be that way because we'll be delivering the `host` and `port` from here in Procfile. **DON'T** PUT THE PARAMETERS INSIDE **app.py** EVEN IF YOU KNOW THOSE VALUES WELL. If it is not like this, the app won't be able to launch after each push and deploy.

Btw, we call Procfile commands using Heroku CLI from terminal this way

~~~~ heroku
heroku run init
heroku run migrate
heroku run web
~~~~

This also can be done without calling the aliases

~~~~
heroku run python manage.py db init
~~~~

To go into the heroku shell

~~~~
heroku run bash
~~~~

`ls -ltr` shows the directory structure, `exit` closes the bash terminal.





## ERROR: alembic.util.CommandError: can't find identifier

[https://stackoverflow.com/questions/32311366/alembic-util-command-error-cant-find-identifier]

Do what is said in the SO thread. You'll need to install PostgreSQL first.

Go to this link [https://devcenter.heroku.com/articles/heroku-postgresql#set-up-postgres-on-windows]

Be **sure** to close everything on mother earth after updating th PATH variable. If everything was correct, you'll be able to call `psql` on terminal. Then do

~~~~
heroku pg:psql
~~~~

You'll then go into the db shell of the heroku database. Now write the commands as instructed in the SO answer and do the rest.



NOTE: If `psql` asks for password, the password you set up during install won't work. Check the SO thread [https://stackoverflow.com/questions/12562928/psql-exe-password-authentication-failed-in-windows]
