import os
from flask import Flask, jsonify, request
import enum
from sqlalchemy import Enum
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
import jwt

# TODO: make sure that only user's loggedin in main app can use this api
# TODO: look into encryption to secure db

# getting the connection string from environment variables
connection_string = os.getenv("POSTGRES_DB")

# NextAuth Secret
SECRET_KEY = os.getenv("AUTH_SECRET")

# token verification middleware

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return jsonify({"message": "Token is missing!"}), 401

        try:
            token = auth_header.split(" ")[1]
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            request.user_id = data["id"]
        except Exception as e:
            return jsonify({"message": "Token is invalid!", "error": str(e)}), 401

        return f(*args, **kwargs)
    return decorated

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
    username = db.Column(db.String(30), nullable=False)

class ExerciseActivity(db.Model):
    __tablename__ = "exercise_activities"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False) 
    activity = db.Column(db.Enum(ActivityEnum), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date, nullable=False)
    calories = db.Column(db.Integer, nullable=False)

# TODO: check if this would overwrite existing tables

# TODO: make into decorator and add as middleware to everything else
# TODO: make sure frontend sends token to flask api end
# try:
#     idinfo = id_token.verify_oauth2_token(token, requests.Request(), "YOUR_GOOGLE_CLIEN_://googleusercontent.com")
#     # user is signed in
# except ValueError:
#     # Invalid token
#     pass


# Create database tables in the PostgreSQL database
with app.app_context():
    db.create_all()

# api routes

# getting all activities of a user
@app.route('/get-all-user-exercises', methods=['GET'])
@token_required
def get_all_user_exercises():
    params = {"id": "1232345", "email": "helloworld@example.com"} # change this to get params from request, think about security, maybe just have this be id and nothing else
    exercises = db.session.execute(db.select(ExerciseActivity)
                                   .join(Users, Users.id == ExerciseActivity.user_id)
                                   .where(Users.id == params.id)
                                   .order_by(ExerciseActivity.date)).scalars()
    return jsonify(exercises)

#TODO: add what error handling
# deleting an activity of a user
@app.route('/delete-exercise-activity', methods=['DELETE'])
@token_required
def delete_activity():
    data = request.get_json()
    delete = db.session.execute(db.delete(ExerciseActivity)
                                .where(ExerciseActivity.id == data.id)).commit()
    return jsonify({})

# TODO: make api endpoint for getting exercise data for charts


if __name__ == "__main__":
    app.run(debug=True)