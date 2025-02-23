from flask import Flask, request, jsonify
from pymongo import MongoClient
import datetime  # Tambahkan import datetime


app = Flask(__name__)

client = MongoClient("mongodb+srv://verlinorayafajri:Marimo.123@aiothinkers.x358i.mongodb.net/?retryWrites=true&w=majority&appName=aiothinkers")

db = client["aiothinkers"]
collection = db["test"]

@app.route("/sensors", methods=["POST"])
def create():
  try:
    data = request.get_json()

    data["timestamp"] = datetime.datetime.utcnow()

    result = collection.insert_one(data)
    return jsonify({
      "message": "Data inserted successfully",
      "_id": str(result.inserted_id),
    }), 201
  except Exception as e:
    return jsonify({"error": str(e)}), 400


# Run Application
if __name__ == "__main__":
  app.run(debug=True, host="0.0.0.0")