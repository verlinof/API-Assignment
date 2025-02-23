from flask import Blueprint, request, jsonify
from src.config.database import SENSOR_COLLECTION
import datetime

collection = SENSOR_COLLECTION
SensorController = Blueprint("SensorController", __name__)

@SensorController.route("/sensors", methods=["GET"])
def index():
    try:
        # Ambil semua data dari MongoDB
        data = list(collection.find().sort("timestamp", -1))

        # Ubah ObjectId ke string agar bisa dikirim sebagai JSON
        for document in data:
            document["_id"] = str(document["_id"])

        return jsonify({
          "message": "Success retrieving data",
          "data": data
        }), 200
    except Exception as e:
        return jsonify({"error": "Internal Server Error"}), 400

@SensorController.route("/avg/rpm", methods=["GET"])
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
        return jsonify({"error": "Internal Server Error"}), 400

@SensorController.route("/avg/moisture", methods=["GET"])
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
        return jsonify({"error": "Internal Server Error"}), 500

@SensorController.route("/sensors", methods=["POST"])
def create():
  try:
    data = request.json

   # Validation
    errors = {}

    if "rpm" not in data:
      errors["rpm"] = "RPM is required"
    if "moisture" not in data:
      errors["moisture"] = "Moisture is required"

    if errors:
      return jsonify({"error": errors}), 400

    data["timestamp"] = datetime.datetime.utcnow()

    result = collection.insert_one(data)
    return jsonify({
      "message": "Data inserted successfully",
      "_id": str(result.inserted_id),
    }), 201
  except Exception as e:
    return jsonify({"error": "Data failed to insert"}), 500


