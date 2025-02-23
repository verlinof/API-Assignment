from flask import Flask, request, jsonify
from pymongo import MongoClient
import datetime  # Tambahkan import datetime


app = Flask(__name__)

client = MongoClient("mongodb+srv://verlinorayafajri:Marimo.123@aiothinkers.x358i.mongodb.net/?retryWrites=true&w=majority&appName=aiothinkers")

db = client["aiothinkers"]
collection = db["test"]

@app.route("/sensors", methods=["GET"])
def index():
    try:
        # Ambil semua data dari MongoDB
        data = list(collection.find())

        # Ubah ObjectId ke string agar bisa dikirim sebagai JSON
        for document in data:
            document["_id"] = str(document["_id"])

        return jsonify({
          "message": "Success retrieving data",
          "data": data
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/avg/rpm", methods=["GET"])
def avg_rpm():
    try:
        # Ambil semua data dari MongoDB
        data = list(collection.find())

        # Hitung rata-rata RPM
        total_rpm = sum(doc["rpm"] for doc in data)
        avg_rpm = total_rpm / len(data)

        return jsonify({
          "message": "Success retrieving data",
          "data": avg_rpm
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/avg/moisture", methods=["GET"])
def avg_moisture():
    try:
        # Ambil semua data dari MongoDB
        data = list(collection.find())

        # Hitung rata-rata Moisture
        total_moisture = sum(doc["moisture"] for doc in data)
        avg_moisture = total_moisture / len(data)

        return jsonify({
          "message": "Success retrieving data",
          "data": avg_moisture
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

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