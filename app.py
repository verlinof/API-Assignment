from flask import Flask, request, jsonify
from pymongo import MongoClient
import datetime 
from src.config import FLASK_RUN_HOST, FLASK_RUN_PORT, FLASK_DEBUG
from src.controllers import SensorController

app = Flask(__name__)

# Register Controller
app.register_blueprint(SensorController)

# Run Application
if __name__ == "__main__":
  app.run(debug=FLASK_DEBUG, host=FLASK_RUN_HOST, port=FLASK_RUN_PORT)