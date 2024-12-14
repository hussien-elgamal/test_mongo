from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
import os
app = Flask(__name__)

# Replace this with your Atlas connection string
app.config["MONGO_URI"] = os.getenv("MONGO_URI")

mongo = PyMongo(app)

@app.route("/")
def welcome():
    return jsonify({"message": "Welcome to the Flask REST API!"})

@app.route("/add_message", methods=["GET"])
def add_message():
    message = request.args.get("message")
    subject = request.args.get("subject")
    class_name = request.args.get("class_name")
    if message:
        mongo.db.messages.insert_one({"message": message, "subject": subject, "class_name": class_name})
        return jsonify({"status": "success", "message": "Message added successfully!"})
    return jsonify({"error": "Missing 'message' parameter"}), 400

@app.route("/messages", methods=["GET"])
def get_messages():
    messages = list(mongo.db.messages.find({}, {"_id": 0}))  # Exclude _id field
    return jsonify(messages)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

