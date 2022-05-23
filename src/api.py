from flask import Flask, request
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)
app.config["DEBUG"] = True

qos_state = "NOT ASSIGNED"

@app.route('/', methods=['GET'])
def index():
    return "NetApp web-server started"

@app.route('/monitoring/callback', methods=['POST'])
def qos_reporter():
    requests.post("http://172.17.0.3:5000/monitoring/callback", json=request.get_json())
    qos_state = request.get_json()['eventReports'][0]['event']
    print("Current state: " + qos_state)
    return qos_state

if __name__ == '__main__':
    print("initiating")
    app.run(host='0.0.0.0', port=5555)

