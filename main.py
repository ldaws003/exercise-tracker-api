import os
from flask import Flask, jsonify
import enum
from sqlalchemy import Enum
from flask_sqlalchemy import SQLAlchemy

# TODO: make sure that only user's loggedin in main app can use this api
# TODO: look into encryption to secure db

# getting the connection string from environment variables
connection_string = os.getenv("POSTGRES_DB")

# Initialize Flask app and set connection string from Vercel's dashboard
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = connection_string

# Initialize SQLAlchemy and defining a simple Book model
db = SQLAlchemy(app)

# defining enum for exercise activity column
class ActivityEnum(enum.Enum):
    RUNNING = "running" 
    WEIGHTS = "weights" 
    WALKING = "walking" 
    BIKING = "biking"


# Defining tables
class Users(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(30), unique=True, nullable=False)

class ExerciseActivity(db.Model):
    __tablename__ = "exercise_activities"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False) 
    activity = db.Column(db.Enum(ActivityEnum), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date, nullable=False)
    calories = db.Column(db.Integer, nullable=False)

# TODO: check if this would overwrite existing tables

# Create database tables in the PostgreSQL database
with app.app_context():
    db.create_all()

# api routes

# getting all activities of a user
@app.route('/get-all-user-exercises', methods=['GET'])
def get_all_user_exercises():
    params = {"id": "1232345", "email": "helloworld@example.com"} # change this to get params from request, think about security, maybe just have this be id and nothing else
    exercises = db.session.execute(db.select(ExerciseActivity)
                                   .join(Users, Users.id == ExerciseActivity.user_id)
                                   .where(Users.id == params.id)
                                   .order_by(ExerciseActivity.date)).scalars()
    return jsonify(exercises)

# deleting an activity of a user
@app.route('/delete-exercise-activity', methods=['DELETE'])
def delete_activity():
    return "Hello World"

# TODO: make api endpoint for getting exercise data for charts


if __name__ == "__main__":
    app.run(debug=True)