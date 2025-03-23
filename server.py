from flask import Flask, request, jsonify
from pymongo import MongoClient

import dotenv
import os

dotenv.load_dotenv('.env')
db_url: str = os.getenv('MONGODB_URI')


app = Flask(__name__)

# Connect to MongoDB
client = MongoClient(db_url)
db = client["bank"]
users_collection = db["users"]

# Insert a sample user if database is empty
if users_collection.count_documents({}) == 0:
    users_collection.insert_one({
        "account_number": "123456789",
        "pin": "1234",
        "name": "John Doe",
        "balance": 1000.00
    })

@app.route("/login", methods=["POST"])
def login():
    """Authenticate user"""
    data = request.json
    user = users_collection.find_one({"account_number": data["account_number"], "pin": data["pin"]})

    if user:
        return jsonify({"success": True, "name": user["name"], "balance": user["balance"]})
    return jsonify({"success": False, "message": "Invalid credentials"}), 401

@app.route("/balance/<account_number>", methods=["GET"])
def get_balance(account_number):
    """Retrieve user balance"""
    user = users_collection.find_one({"account_number": account_number})
    if user:
        return jsonify({"balance": user["balance"]})
    return jsonify({"error": "Account not found"}), 404

@app.route("/withdraw", methods=["POST"])
def withdraw():
    """Withdraw money"""
    data = request.json
    user = users_collection.find_one({"account_number": data["account_number"]})

    if user and user["balance"] >= data["amount"]:
        new_balance = user["balance"] - data["amount"]
        users_collection.update_one({"account_number": data["account_number"]}, {"$set": {"balance": new_balance}})
        return jsonify({"success": True, "new_balance": new_balance})

    return jsonify({"success": False, "message": "Insufficient funds"}), 400

@app.route("/deposit", methods=["POST"])
def deposit():
    """Deposit money"""
    data = request.json
    user = users_collection.find_one({"account_number": data["account_number"]})

    if user:
        new_balance = user["balance"] + data["amount"]
        users_collection.update_one({"account_number": data["account_number"]}, {"$set": {"balance": new_balance}})
        return jsonify({"success": True, "new_balance": new_balance})

    return jsonify({"error": "Account not found"}), 404

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
