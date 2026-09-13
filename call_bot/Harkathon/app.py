from flask import Flask, render_template, request, jsonify
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Configure your backend API URL
BACKEND_URL = os.getenv('BACKEND_URL', 'http://localhost:5000')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/talk', methods=['POST'])
def start_talking():
    try:
        data = request.json
        try:
            response = requests.post(f"{BACKEND_URL}/api/talk", json=data, timeout=5)
            try:
                return jsonify(response.json()), response.status_code
            except ValueError:
                return jsonify({
                    "message": "Hello! I'm your talking bot. How can I help you today?"
                }), 200
        except requests.exceptions.ConnectionError:
            return jsonify({
                "error": "Backend server is not running. Please start the backend server at " + BACKEND_URL
            }), 503
        except requests.exceptions.Timeout:
            return jsonify({
                "error": "Backend server is taking too long to respond. Please try again."
            }), 504
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=3000) 