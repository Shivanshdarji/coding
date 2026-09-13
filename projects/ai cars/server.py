from flask import Flask, render_template
from flask_socketio import SocketIO
import math

from flask import Flask, render_template

app = Flask(__name__, template_folder='templates', static_folder='static')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
socketio = SocketIO(app, cors_allowed_origins="*")

# Store active cars {id: (lat, lon)}
cars = {}

@socketio.on("connect")
def handle_connect():
    print("New client connected")

@socketio.on("update_location")
def handle_location(data):
    cars[data["id"]] = (data["lat"], data["lon"])
    
    # Check distances (10m threshold)
    for car_id, (lat, lon) in cars.items():
        if car_id != data["id"]:
            # Convert degrees to approximate meters
            distance = math.dist((data["lat"], data["lon"]), (lat, lon)) * 111320
            if distance < 10:
                socketio.emit("emergency_stop", {"car_id": data["id"]})

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    print("🚗 Server running at http://localhost:5001")
    socketio.run(app, host="0.0.0.0", port=5001, debug=True)