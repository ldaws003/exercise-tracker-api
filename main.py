import os
from flask import Flask
import enum
from sqlalchemy import Enum
from flask_sqlalchemy import SQLAlchemy

# getting the connection string from environment variables
connection_string = os.getenv("POSTGRES_DB")

# Initialize Flask app and set connection string from Vercel's dashboard
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = connection_string

# Initialize SQLAlchemy and defining a simple Book model
db = SQLAlchemy(app)

# class Book(db.Model):
#     book_id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String)

# defining enum for exercise activity column
class ActivityEnum(enum.Enum):
    RUNNING = "running" 
    WEIGHTS = "weights" 
    WALKING = "walking" 
    BIKING = "biking"

class Users(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)


class ExerciseActivity(db.Model):
    __tablename__ = "exercise_activities"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False) 
    activity = db.Column(db.Enum(ActivityEnum), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date, nullable=False)
    calories = db.Column(db.Integer, nullable=False)
    pass


# TODO: check if this would overwrite existing tables
# Create database tables in the PostgreSQL database
with app.app_context():
    db.create_all()

# api routes

# getting all activities of a user
@app.route('/get-all-user-exercises', methods=['GET'])
def get_exercises():
    return "Hello World"


if __name__ == "__main__":
    app.run(debug=True)