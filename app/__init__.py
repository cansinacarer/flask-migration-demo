import os

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_sslify import SSLify

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

# DB Config
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "postgresql://flask_db_user:1234@test.cansin.net:5432/flask_db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
sslify = SSLify(app)


# Create the table if it doesn't exist
@app.before_first_request
def initialize_database():
    db.create_all()


# Table definition
class Test(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(100))

    def __init__(
        self,
        message,
    ):
        self.message = message

    def save(self):

        # inject self into db session
        db.session.add(self)

        # commit change and save the object
        db.session.commit()

        return self


# Add a test message to the database as a record
@app.before_first_request
def write_test_message():
    test_user = Test(message="test message from database is read successfully")
    test_user.save()


# Try to read the test message from the database and show it in the home page
@app.route("/")
def index():
    try:
        first_record = Test.query.first()
        message = first_record.message
    except:
        message = "database connection failed"
    return message
