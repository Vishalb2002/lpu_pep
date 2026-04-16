from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient

app = Flask(__name__)

# MongoDB connection
MONGO_URL = "mongodb://admin:qwerty@localhost:27017"
client = MongoClient(MONGO_URL)

db = client["abhi"]
collection = db["users"]

# Home page (form)
@app.route("/")
def home():
    return render_template("index.html")

# Show users in browser
@app.route("/getUsers")
def get_users_page():
    users = list(collection.find({}, {"_id": 0}))
    return render_template("users.html", users=users)

# API: Get users (JSON)
@app.route("/api/getUsers", methods=["GET"])
def get_users():
    users = list(collection.find({}, {"_id": 0}))
    return jsonify(users)

# API: Add user
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
    app.run(port=5050, debug=True)