from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
import os

app = Flask(__name__)

# Load environment variables
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME", "abhi")

# MongoDB connection
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db["users"]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/getUsers")
def get_users_page():
    users = list(collection.find({}, {"_id": 0}))
    return render_template("users.html", users=users)

@app.route("/api/getUsers", methods=["GET"])
def get_users():
    users = list(collection.find({}, {"_id": 0}))
    return jsonify(users)

@app.route("/addUser", methods=["POST"])
def add_user():
    data = request.form

    user = {
        "name": data.get("name"),
        "email": data.get("email"),
        "contact": data.get("contact"),
        "password": data.get("password")
    }

    collection.insert_one(user)
    return render_template("index.html", message="User added successfully!")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050)